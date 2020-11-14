from django.contrib import admin
from .models import Vehicle, Access


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('plate',)}

@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    pass