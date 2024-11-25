from django.urls import path
from . import api

urlpatterns = [
    # Existing URLs
    path('farmhouses/', api.farmhouse_list, name='farmhouse-list'),
    path('farmhouses/<int:pk>/', api.farmhouse_detail, name='farmhouse-detail'),
    path('bookings/', api.booking_list, name='booking-list'),
    path('bookings/<int:booking_id>/review/', api.create_review, name='create-review'),
    
    # New URLs for slug and images
    path('farmhouses/<str:slug>/', api.farmhouse_by_slug, name='farmhouse-by-slug'),
    path('farmhouses/<int:farmhouse_id>/images/', api.farmhouse_images, name='farmhouse-images'),
    path('farmhouse-images/<int:image_id>/', api.delete_farmhouse_image, name='delete-farmhouse-image'),
]