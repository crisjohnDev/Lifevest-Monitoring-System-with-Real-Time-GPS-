from django.urls import path
from .views import lora_data_receiver

urlpatterns = [
    path('api/lora-data/', lora_data_receiver, name='lora_data_receiver'),
]