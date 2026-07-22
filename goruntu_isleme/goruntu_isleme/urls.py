"""
URL configuration for goruntu_isleme project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'goruntu_isleme'

urlpatterns = [
    path('', views.home, name='home'),  # Kök URL ana sayfaya yönlendirilecek
    path('admin/', admin.site.urls),
    path('upload/', views.upload_video, name='upload_video'),
    path('videos/', views.video_list, name='video_list'),
    path('report/<int:video_id>/', views.video_report, name='video_report'),
    path('video/<int:video_id>/delete/', views.delete_video, name='delete_video'),
    path('calculate-route/', views.calculate_route, name='calculate_route'),
    path('map/', views.map_view, name='map_view'),
    path('save-route/', views.save_route, name='save_route'),
    path('routes/', views.route_list, name='route_list'),
    path('delete-route/<int:route_id>/', views.delete_route, name='delete_route'),  # Güzergah silme URL'si
    path('canli-takip/', views.canli_takip, name='canli_takip'),  # Canlı takip sayfası
    path('dronelar/', views.drone_list, name='drone_list'),  # Dronelar sayfası

   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


