from rest_framework import serializers
from django.db.models import Avg
from .models import Station, Review, AspectSentiment


class StationSerializer(serializers.ModelSerializer):
    """Basic station info for station list and search"""
    review_count = serializers.IntegerField(read_only=True)
    avg_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Station
        fields = ['id', 'name', 'line', 'review_count', 'avg_rating']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'overall_rating', 'review_text', 'created_at', 'helpful_count']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new reviews"""
    class Meta:
        model = Review
        fields = ['station', 'overall_rating', 'review_text']


class AspectSentimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AspectSentiment
        fields = ['id', 'aspect', 'sentiment', 'review']


class StationDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with recent reviews + stats"""
    recent_reviews = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = ['id', 'name', 'line', 'recent_reviews', 'stats']

    def get_recent_reviews(self, obj):
        reviews = Review.objects.filter(station=obj).order_by('-created_at')[:10]
        return ReviewSerializer(reviews, many=True).data

    def get_stats(self, obj):
        reviews = Review.objects.filter(station=obj)
        if not reviews.exists():
            return None

        total = reviews.count()
        avg_rating = round(reviews.aggregate(avg=Avg('overall_rating'))['avg'] or 0, 1)
        dist = {str(i): reviews.filter(overall_rating=i).count() for i in range(1, 6)}

        # Dummy aspects (replace with AspectStats if you implement later)
        aspects = {
            "Cleanliness": {"score": 4.1, "sentiment": "positive", "trend": "+0.3", "percentage": 82},
            "Safety": {"score": 4.5, "sentiment": "positive", "trend": "+0.1", "percentage": 90},
            "Facilities": {"score": 3.9, "sentiment": "neutral", "trend": "-0.1", "percentage": 75}
        }

        recent_trends = {
            "thisMonth": "+0.2",
            "lastMonth": "+0.1",
            "sentiment": "improving"
        }

        return {
            "overallRating": avg_rating,
            "totalReviews": total,
            "reviewDistribution": dist,
            "aspects": aspects,
            "recentTrends": recent_trends,
        }
