from django.contrib import admin
from django.urls import path, include
from apiApp.views import api_save_access, api_receive_image

urlpatterns = [
    path('save-access/', api_save_access, name='api_save_access'),
    path('receive-images/', api_receive_image, name='api_receive_image'),
]
