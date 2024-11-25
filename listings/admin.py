# from django.contrib import admin
from .models import Farmhouse, FarmhouseImage, Booking, Review, UserProfile

@admin.register(Farmhouse)
class FarmhouseAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'city', 'owner', 'bedrooms', 'created_at','slug')
    list_filter = ('city', 'has_pool', 'has_wifi', 'has_air_conditioning')
    search_fields = ('name', 'city', 'description')
    prepopulated_fields = {'slug': ('name', 'city')}

@admin.register(FarmhouseImage)
class FarmhouseImageAdmin(admin.ModelAdmin):
    list_display = ('id','farmhouse', 'is_primary', 'uploaded_at')
    # list_filter = ('is_primary', 'uploaded_at')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','booking_number', 'farmhouse', 'guest', 'status')
    # list_filter = ('status',)
    search_fields = ('booking_number', 'guest__username', 'farmhouse__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id','farmhouse', 'reviewer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'phone_number')
    search_fields = ('user__username', 'phone_number')