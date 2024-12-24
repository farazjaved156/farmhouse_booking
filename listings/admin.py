from django.contrib import admin
from .models import Farmhouse, FarmhouseImage, Booking, Review, UserProfile, FarmhousePricing
from decimal import Decimal

# @admin.register(Farmhouse)
# class FarmhouseAdmin(admin.ModelAdmin):
#     list_display = ('id','name', 'city', 'owner', 'bedrooms', 'created_at','slug')
#     list_filter = ('city', 'has_pool', 'has_wifi', 'has_air_conditioning')
#     search_fields = ('name', 'city', 'description')
#     prepopulated_fields = {'slug': ('name', 'city')}
    
class FarmhousePricingInline(admin.TabularInline):
    model = FarmhousePricing
    extra = 0  # No extra blank rows by default
    readonly_fields = ('date', 'shift', 'price')
    can_delete = False


@admin.register(Farmhouse)
class FarmhouseAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'city', 'owner', 'bedrooms', 'created_at','slug')
    list_filter = ('city', 'has_pool', 'has_wifi', 'has_air_conditioning')
    search_fields = ('name', 'city', 'description')
    prepopulated_fields = {'slug': ('name', 'city')}
    inlines = [FarmhousePricingInline]
    actions = ['add_prices_for_next_four_months']

    def add_prices_for_next_four_months(self, request, queryset):
        """
        Admin action to add pricing for the next 4 months for selected farmhouses.
        """
        day_price = Decimal('200.00')  # Set the day shift price
        night_price = Decimal('150.00')  # Set the night shift price

        for farmhouse in queryset:
            FarmhousePricing.add_prices_for_next_four_months(
                farmhouse=farmhouse,
                day_price=day_price,
                night_price=night_price
            )
        self.message_user(
            request,
            f"Pricing added for the next 4 months for {queryset.count()} farmhouse(s)."
        )

    add_prices_for_next_four_months.short_description = "Add prices for the next 4 months"


@admin.register(FarmhousePricing)
class FarmhousePricingAdmin(admin.ModelAdmin):
    list_display = ('id', 'farmhouse', 'date', 'shift', 'price')
    # list_filter = ('farmhouse', 'shift', 'date')
    # search_fields = ('farmhouse__name', 'shift')

@admin.register(FarmhouseImage)
class FarmhouseImageAdmin(admin.ModelAdmin):
    list_display = ('id','farmhouse', 'is_primary', 'uploaded_at')
    # list_filter = ('is_primary', 'uploaded_at')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','booking_number', 'farmhouse', 'guest', 'status')
    # list_filter = ('status',)
    search_fields = ('booking_number', 'guest__username', 'farmhouse__name')
#Open to work
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id','farmhouse', 'reviewer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'phone_number')
    search_fields = ('user__username', 'phone_number')
