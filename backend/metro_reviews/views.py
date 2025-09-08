from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Station, Review, AspectSentiment
from .serializers import (
    StationSerializer, ReviewSerializer, ReviewCreateSerializer,
    StationDetailSerializer, AspectSentimentSerializer
)


@api_view(['GET'])
def station_list(request):
    """Get all active stations with basic stats"""
    stations = Station.objects.filter(is_active=True).annotate(
        review_count=Count('review'),
        avg_rating=Avg('review__overall_rating')
    ).order_by('name')

    serializer = StationSerializer(stations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def station_detail(request, station_id):
    """Get detailed station info with reviews and stats"""
    station = get_object_or_404(Station, id=station_id, is_active=True)
    serializer = StationDetailSerializer(station)
    return Response(serializer.data)


@api_view(['POST'])
def create_review(request):
    """Create a new review"""
    serializer = ReviewCreateSerializer(data=request.data)
    if serializer.is_valid():
        review = serializer.save()
        return Response(
            ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def recent_reviews(request):
    """Get recent reviews across all stations"""
    days = int(request.GET.get('days', 7))
    limit = int(request.GET.get('limit', 20))

    from datetime import datetime, timedelta
    since_date = datetime.now() - timedelta(days=days)

    reviews = Review.objects.filter(
        created_at__gte=since_date
    ).select_related('station').order_by('-created_at')[:limit]

    return Response(ReviewSerializer(reviews, many=True).data)


@api_view(['GET'])
def dashboard_analytics(request):
    """Get overview analytics for dashboard"""
    total_stations = Station.objects.filter(is_active=True).count()
    total_reviews = Review.objects.count()

    top_stations = Station.objects.filter(is_active=True).annotate(
        avg_rating=Avg('review__overall_rating'),
        review_count=Count('review')
    ).filter(review_count__gte=5).order_by('-avg_rating')[:5]

    # Aspect overview (dummy until you implement AspectStats)
    aspect_overview = []
    aspects = [choice[0] for choice in AspectSentiment.ASPECT_CHOICES]

    for aspect in aspects:
        positive_count = AspectSentiment.objects.filter(
            aspect=aspect, sentiment='positive'
        ).count()
        total_count = AspectSentiment.objects.filter(aspect=aspect).count()
        satisfaction = (positive_count / total_count * 100) if total_count > 0 else 0

        aspect_overview.append({
            'aspect': aspect,
            'satisfaction_percentage': round(satisfaction, 1),
            'total_mentions': total_count
        })

    return Response({
        'overview': {
            'total_stations': total_stations,
            'total_reviews': total_reviews,
            'avg_system_rating': Review.objects.aggregate(
                avg=Avg('overall_rating')
            )['avg'] or 0
        },
        'top_stations': StationSerializer(top_stations, many=True).data,
        'aspect_overview': aspect_overview
    })


@api_view(['POST'])
def mark_review_helpful(request, review_id):
    """Mark a review as helpful"""
    review = get_object_or_404(Review, id=review_id)
    review.helpful_count += 1
    review.save()
    return Response({'helpful_count': review.helpful_count})


@api_view(['GET'])
def search_stations(request):
    """Search stations by name or line"""
    query = request.GET.get('q', '').strip()
    if not query:
        return Response([])

    stations = Station.objects.filter(
        Q(name__icontains=query) | Q(line__icontains=query),
        is_active=True
    ).annotate(
        review_count=Count('review'),
        avg_rating=Avg('review__overall_rating')
    )[:10]

    return Response(StationSerializer(stations, many=True).data)
