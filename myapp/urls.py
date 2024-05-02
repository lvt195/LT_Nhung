from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.QRView.as_view(), name='qr'),
    path('generate_qr/', views.generate_qr_view, name='generate_qr'),
    path('read_qr/', views.read_qr_view, name='read_qr'),
    path('qr_scanner/', views.generate_qr_data, name='qr_scanner'),
    path('qr_display/', views.qr_display_view, name='qr_display'),
] 