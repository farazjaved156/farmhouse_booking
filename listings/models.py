from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date, timedelta
from decimal import Decimal

class Farmhouse(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farmhouses')
    description = models.TextField()
    address = models.TextField()
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    max_guests = models.PositiveIntegerField()
    square_feet = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Amenities
    has_pool = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    has_kitchen = models.BooleanField(default=True)
    has_air_conditioning = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        created = not self.pk  # Check if this is a new instance
        super().save(*args, **kwargs)  # Save first to get the ID
        
        if created or not self.slug:  # Generate slug for new instances or if slug is empty
            self.slug = f"{slugify(self.name)}-{slugify(self.city)}-{self.pk}"
            super().save(*args, **kwargs)  # Save again with the generated slug

    def __str__(self):
        return f"{self.name} in {self.city}"

    class Meta:
        verbose_name_plural = "Farmhouses"
        ordering = ['-created_at']
        
class FarmhousePricing(models.Model):
    SHIFT_CHOICES = [
        ('day', 'Day Shift (8 AM - 7 PM)'),
        ('night', 'Night Shift (8 PM - 7 AM)')
    ]

    farmhouse = models.ForeignKey(
        'Farmhouse', on_delete=models.CASCADE, related_name='pricing_options'
    )
    date = models.DateField()
    shift = models.CharField(max_length=5, choices=SHIFT_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['farmhouse', 'date', 'shift']
        verbose_name_plural = "Farmhouse Pricing Options"

    def __str__(self):
        return f"{self.farmhouse.name} - {self.date} {self.get_shift_display()} Price"

    @classmethod
    def add_prices_for_next_four_months(cls, farmhouse, day_price, night_price):
        start_date = date.today()
        end_date = start_date + timedelta(days=120)  # Approx. 4 months

        with transaction.atomic():  # Ensure atomicity
            for single_date in (start_date + timedelta(days=i) for i in range((end_date - start_date).days)):
                # Add day shift pricing
                cls.objects.update_or_create(
                    farmhouse=farmhouse,
                    date=single_date,
                    shift='day',
                    defaults={'price': day_price}
                )
                # Add night shift pricing
                cls.objects.update_or_create(
                    farmhouse=farmhouse,
                    date=single_date,
                    shift='night',
                    defaults={'price': night_price}
                )

class FarmhouseImage(models.Model):
    farmhouse = models.ForeignKey(Farmhouse, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/static/images/')
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Booking(models.Model):
    SHIFT_CHOICES = [
        ('day', 'Day Shift (8 AM - 7 PM)'),
        ('night', 'Night Shift (8 PM - 7 AM)')
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]

    booking_number = models.CharField(max_length=35, unique=True, editable=False)
    farmhouse = models.ForeignKey(Farmhouse, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    shift = models.CharField(max_length=5, choices=SHIFT_CHOICES)
    number_of_guests = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    special_requests = models.TextField(blank=True)

    def __str__(self):
        return f"{self.booking_number} - {self.guest.username}'s {self.shift} booking at {self.farmhouse.name}"

    class Meta:
        unique_together = ['farmhouse', 'booking_date', 'shift']

class Review(models.Model):
    farmhouse = models.ForeignKey(Farmhouse, on_delete=models.CASCADE, related_name='reviews')
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.farmhouse.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"