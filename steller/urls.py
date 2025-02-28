"""steller URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
#
from .views import home_page, send_images, save_image
#

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', home_page, name='dashboard_index'),
    path('send-images/', send_images, name='send_images_index'),
    path('save_image/', save_image, name='save_images_index'),
    path('auth/', include('authApp.urls')),
    path('controller/', include('accessApp.urls')),
    path('api/v1/', include('apiApp.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'steller.views.handler404'
handler403 = 'steller.views.handler403'
handler500 = 'steller.views.handler500'
