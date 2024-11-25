from rest_framework import serializers
from django.db.models import Avg
from .models import Farmhouse, FarmhouseImage, Booking, Review, UserProfile
from django.contrib.auth.models import User
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class FarmhouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmhouseImage
        fields = ['id', 'image', 'is_primary', 'caption']

class FarmhouseSerializer(serializers.ModelSerializer):
    images = FarmhouseImageSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Farmhouse
        fields = '__all__'
        read_only_fields = ['slug', 'owner']

    def get_average_rating(self, obj):
        return obj.reviews.aggregate(Avg('rating'))['rating__avg']

class BookingSerializer(serializers.ModelSerializer):
    guest = UserSerializer(read_only=True)
    farmhouse = FarmhouseSerializer(read_only=True)
    farmhouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Farmhouse.objects.all(),
        write_only=True,
        source='farmhouse'
    )
    shift_display = serializers.CharField(source='get_shift_display', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['booking_number', 'total_price', 'guest']

    def validate(self, data):
        # Check if the date is not in the past
        if data['booking_date'] < datetime.now().date():
            raise serializers.ValidationError(
                "Booking date cannot be in the past"
            )

        # Check if farmhouse is available for this date and shift
        existing_booking = Booking.objects.filter(
            farmhouse=data['farmhouse'],
            booking_date=data['booking_date'],
            shift=data['shift'],
            status='confirmed'
        )
        
        if existing_booking.exists():
            raise serializers.ValidationError(
                f"This {data['shift']} shift is already booked for the selected date"
            )

        # Validate number of guests
        if data['number_of_guests'] > data['farmhouse'].max_guests:
            raise serializers.ValidationError(
                f"Maximum {data['farmhouse'].max_guests} guests allowed"
            )

        return data

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['reviewer']

    def validate(self, data):
        # Ensure user can only review after their stay
        if not Booking.objects.filter(
            guest=self.context['request'].user,
            farmhouse=data['farmhouse'],
            status='completed'
        ).exists():
            raise serializers.ValidationError(
                "You can only review after completing your stay"
            )
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user']