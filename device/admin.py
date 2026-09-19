from django.contrib import admin
from .models import LoraRecord

@admin.register(LoraRecord)
class LoraRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'count', 'gps_status', 'latitude', 'longitude', 'rssi', 'snr', 'timestamp')
    search_fields = ('packet_raw',)
    list_filter = ('gps_status', 'timestamp')