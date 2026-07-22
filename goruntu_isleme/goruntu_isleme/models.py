from django.db import models
from django.utils import timezone

class Video(models.Model):
    video_file = models.FileField(upload_to='videos/') 
    upload_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255,default="İsim Giriniz")
    description = models.TextField(default="Açıklama Giriniz")  # Set default value here

    def __str__(self):
        return f"Video {self.id}"
    


class Route(models.Model):
    name = models.CharField(max_length=255)  # Güzergahın başlığı
    coordinates = models.JSONField()  # Koordinatlar (JSON formatında)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name
    
class Drone(models.Model):
    name = models.CharField(max_length=100, default="İsim Giriniz")
    guc_turu = models.CharField(max_length=100, default="Güç Türü Giriniz")
    flight_range = models.CharField(max_length=100,null=True)  
    payload_capacity = models.CharField(max_length=100,null=True)  
    camera_type = models.CharField(max_length=100, default="Kamera Türü Giriniz")
    photo = models.ImageField(upload_to='drone_photos/', blank=True, null=True) 
    sicaklik = models.CharField(max_length=100, default="Sıcaklık Giriniz")
    iletim_araligi = models.CharField(max_length=100,null=True)  
    max_ucus_sure = models.CharField(max_length=100,null=True)  
    koruma_derecesi = models.CharField(max_length=100,null=True)  


    def __str__(self):
        return self.name