from django.urls import path
from .views import (
    VehicleListView,
    export_vehicles,
    print_vehicles,
    VehicleCreateView,
    VehicleUpdateView,
    VehicleDeleteView,
    # Access
    AccessListView,
    AccessTodayListView,
    AccessNotExitListView,
    export_access,
    print_access,
    AccessCreateView,
    AccessUpdateView,
)

urlpatterns = [
    path('vehicle/', VehicleListView.as_view(), name='vehicle_index'),
    path('export/vehicle', export_vehicles, name='export_vehicles'),
    path('print/vehicle', print_vehicles, name='print_vehicles'),
    path('vehicle/new/', VehicleCreateView.as_view(), name='vehicle_new'),
    path('vehicle/<slug:slug>/edit/', VehicleUpdateView.as_view(), name='vehicle_edit'),
    path('vehicle/<slug:slug>/delete/', VehicleUpdateView.as_view(), name='vehicle_delete'),
    #
    path('access/', AccessListView.as_view(), name='access_index'),
    path('access/today', AccessTodayListView.as_view(), name='access_today_index'),
    path('access/not-exit', AccessNotExitListView.as_view(), name='access_today_index'),
    path('export/access', export_access, name='export_access'),
    path('print/access', print_access, name='print_access'),
    path('access/new/', AccessCreateView.as_view(), name='access_new'),
    path('access/<int:pk>/edit/', AccessUpdateView.as_view(), name='access_edit'),
]
