from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Farmhouse, Booking, Review, FarmhouseImage
from .serializers import (
    FarmhouseSerializer, 
    BookingSerializer, 
    ReviewSerializer,
    FarmhouseImageSerializer
)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def farmhouse_list(request):
    if request.method == 'GET':
        farmhouses = Farmhouse.objects.all()
        serializer = FarmhouseSerializer(farmhouses, many=True)
        return JsonResponse({
            'data': serializer.data,
        })
    
    elif request.method == 'POST':
        serializer = FarmhouseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def booking_list(request):
    if request.method == 'GET':
        bookings = Booking.objects.filter(guest=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return JsonResponse({
            'data': serializer.data,
        })
    
    elif request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            # Calculate total price based on shift
            farmhouse = serializer.validated_data['farmhouse']
            shift = serializer.validated_data['shift']
            price = farmhouse.night_shift_price if shift == 'night' else farmhouse.day_shift_price
            
            serializer.save(
                guest=request.user,
                total_price=price
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def farmhouse_detail(request, pk):
    farmhouse = get_object_or_404(Farmhouse, pk=pk)
    
    if request.method == 'GET':
        serializer = FarmhouseSerializer(farmhouse)
        return JsonResponse({
            'data': serializer.data,
        })
    
    elif request.method in ['PUT', 'DELETE']:
        if request.user != farmhouse.owner:
            return Response(
                {"error": "You don't have permission to modify this farmhouse"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if request.method == 'PUT':
            serializer = FarmhouseSerializer(farmhouse, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            farmhouse.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, guest=request.user)
    
    if Review.objects.filter(booking=booking).exists():
        return Response(
            {"error": "You have already reviewed this booking"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = ReviewSerializer(
        data=request.data, 
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save(
            reviewer=request.user,
            farmhouse=booking.farmhouse,
            booking=booking
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def farmhouse_by_slug(request, slug):
    farmhouse = get_object_or_404(Farmhouse, slug=slug)
    serializer = FarmhouseSerializer(farmhouse)
    return JsonResponse({
        'data': serializer.data,
    })

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
@parser_classes([MultiPartParser, FormParser])
def farmhouse_images(request, farmhouse_id):
    farmhouse = get_object_or_404(Farmhouse, id=farmhouse_id)
    
    if request.method == 'GET':
        images = FarmhouseImage.objects.filter(farmhouse=farmhouse)
        serializer = FarmhouseImageSerializer(images, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Check if user is the owner
        if request.user != farmhouse.owner:
            return Response(
                {"error": "Only the owner can add images"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Handle primary image logic
        is_primary = request.data.get('is_primary', False)
        if is_primary:
            # Set all other images as non-primary
            FarmhouseImage.objects.filter(farmhouse=farmhouse).update(is_primary=False)
        
        serializer = FarmhouseImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(farmhouse=farmhouse)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_farmhouse_image(request, image_id):
    image = get_object_or_404(FarmhouseImage, id=image_id)
    
    # Check if user is the owner of the farmhouse
    if request.user != image.farmhouse.owner:
        return Response(
            {"error": "Only the owner can delete images"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    image.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)