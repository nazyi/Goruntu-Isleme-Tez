
# admin.py
from django.contrib import admin
from .models import Drone

@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
    list_display = ('name', 'flight_range', 'payload_capacity','camera_type','photo','sicaklik','iletim_araligi','max_ucus_sure','guc_turu','koruma_derecesi')
