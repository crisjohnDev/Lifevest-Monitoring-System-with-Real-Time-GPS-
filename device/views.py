import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import LoraRecord

def parse_packet_string(packet_str):
    """Helper to parse key-value pairs separated by commas."""
    data = {}
    parts = packet_str.split(',')
    for part in parts:
        if '=' in part:
            key, val = part.split('=', 1)
            data[key.strip()] = val.strip()
    return data

@csrf_exempt
def lora_data_receiver(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            packet_raw = body.get('packet', '')
            rssi = body.get('rssi')
            snr = body.get('snr')

            # Parse individual fields out of the LoRa message string
            parsed = parse_packet_string(packet_raw)
            count = int(parsed.get('COUNT')) if parsed.get('COUNT') and parsed.get('COUNT').isdigit() else None
            gps_status = parsed.get('GPS')
            latitude = float(parsed.get('LAT')) if parsed.get('LAT') else None
            longitude = float(parsed.get('LON')) if parsed.get('LON') else None

            # Save record to database
            record = LoraRecord.objects.create(
                packet_raw=packet_raw,
                count=count,
                gps_status=gps_status,
                latitude=latitude,
                longitude=longitude,
                rssi=rssi,
                snr=snr
            )

            return JsonResponse({
                "status": "success", 
                "message": "Packet saved and parsed successfully",
                "record_id": record.id
            }, status=201)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)


def lora_data_list(request):
    records = LoraRecord.objects.all().order_by('-timestamp')[:20]
    data = []
    for r in records:
        data.append({
            "id": r.id,
            "count": r.count,
            "gps_status": r.gps_status,
            "latitude": r.latitude,
            "longitude": r.longitude,
            "rssi": r.rssi,
            "snr": r.snr,
            "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    return JsonResponse({"records": data})