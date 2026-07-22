from django.shortcuts import render, redirect, get_object_or_404
from .forms import VideoUploadForm
from .models import Video
from .utils.analyze_video import analyze_video
import plotly.express as px
import plotly.io as pio
import os
from django.conf import settings
from .models import Drone
from .models import Video, Route
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import itertools
import math
import heapq



def home(request):
    video_count = Video.objects.count()  
    route_count = Route.objects.count()
    videos = Video.objects.all().order_by('-upload_date')[:3]  
    routes = Route.objects.all().order_by('-created_at')[:3]  
    return render(request, 'home.html', {'videos': videos, 'routes': routes, 'video_count': video_count, 'route_count': route_count})

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('video_list')  
        else:
            print("Form hatalı:", form.errors)  
    else:
        form = VideoUploadForm()
    return render(request, 'upload_video.html', {'form': form})

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})

def video_report(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video_path = video.video_file.path
    
    processed_video_filename = f"processed_{video.video_file.name.split('/')[-1]}"  
    processed_videos_path = os.path.join(settings.MEDIA_URL, 'processed_videos', processed_video_filename)

    output_path = os.path.join(settings.MEDIA_ROOT, 'processed_videos', processed_video_filename) 
    detections = analyze_video(video_path, output_path)
    
    label_data = {}
    for detection in detections:
        label = detection['label']
        timestamp = detection['timestamp']
        coordinates = detection['coordinates']

        if label not in label_data:
            label_data[label] = []

        label_data[label].append({
            'timestamp': timestamp,
            'coordinates': coordinates
        })
    
    label_counts = {label: len(data) for label, data in label_data.items()}

    fig, ax = plt.subplots()
    ax.pie(label_counts.values(), labels=label_counts.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    pie_chart_data = base64.b64encode(buf.read()).decode('utf-8')

    return render(request, 'video_report.html', {
        'processed_videos_path': processed_videos_path,
        'label_data': label_data,
        'pie_chart_data': pie_chart_data
    })

def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if video.video_file:
        video_file_path = os.path.join(settings.MEDIA_ROOT, video.video_file.name)
        if os.path.exists(video_file_path):
            os.remove(video_file_path)

    video.delete()

    return redirect('video_list') 

def canli_takip(request):
    return render(request, 'canli_takip.html') 

def drone_list(request):
    drones = Drone.objects.all()  
    return render(request, 'drone_list.html', {'drones': drones})

def a_star(start, goal, coordinates):
    open_list = []
    closed_list = set()
    
    g = {start: 0}  
    h = {start: distance(coordinates[start], coordinates[goal])}  
    f = {start: g[start] + h[start]}  
    
    parent = {start: None}  
    
    heapq.heappush(open_list, (f[start], start))

    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1] 
        
        closed_list.add(current)
        
        for neighbor in range(len(coordinates)):
            if neighbor in closed_list:
                continue
            
            tentative_g = g[current] + distance(coordinates[current], coordinates[neighbor])
            
            if neighbor not in g or tentative_g < g[neighbor]:
                g[neighbor] = tentative_g
                h[neighbor] = distance(coordinates[neighbor], coordinates[goal])
                f[neighbor] = g[neighbor] + h[neighbor]
                parent[neighbor] = current
                heapq.heappush(open_list, (f[neighbor], neighbor))
    
    return None  

def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def find_shortest_path(coordinates):
    
    distance_matrix = [[distance(coord1, coord2) for coord2 in coordinates] for coord1 in coordinates]

    min_distance = float('inf')
    best_path = []

    for perm in itertools.permutations(range(len(coordinates))):
        current_distance = 0
        for i in range(len(perm) - 1):
            current_distance += distance_matrix[perm[i]][perm[i + 1]]
        
        if current_distance < min_distance:
            min_distance = current_distance
            best_path = perm

    return [coordinates[i] for i in best_path]

def calculate_route(request):
    if request.method == 'POST':
        try:
            coordinates = json.loads(request.POST.get('coordinates'))  # JSON verisini al
        except Exception as e:
            return JsonResponse({'error': f'Veri işlenemedi: {str(e)}'}, status=400)

        if len(coordinates) < 2:
            return JsonResponse({'error': 'En az iki nokta gereklidir'}, status=400)

        path = find_shortest_path(coordinates)

        if path:
            path_with_order = [{"index": i + 1, "coords": point} for i, point in enumerate(path)]
            return JsonResponse({'route': path_with_order})
        else:
            return JsonResponse({'error': 'Yol bulunamadı'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def map_view(request):
    return render(request, 'map.html')




@csrf_exempt
def save_route(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            route_name = data.get('name')
            coordinates = data.get('coordinates')

            # Yeni güzergahı kaydet
            route = Route.objects.create(name=route_name, coordinates=coordinates)

            return JsonResponse({'message': 'Güzergah başarıyla kaydedildi!', 'route_id': route.id}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
def route_list(request):
    routes = Route.objects.all().order_by('-created_at')  # En son kaydedilen güzergah önce gelsin
    return render(request, 'route_list.html', {'routes': routes})

def delete_route(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    route.delete()
    return JsonResponse({'message': 'Route deleted successfully'}, status=200)