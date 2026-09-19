from django.db import models

class LoraRecord(models.Model):
    packet_raw = models.TextField()
    count = models.IntegerField(null=True, blank=True)
    gps_status = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    rssi = models.IntegerField()
    snr = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Packet #{self.count} - RSSI: {self.rssi} dBm"