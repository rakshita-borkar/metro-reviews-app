# models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Station(models.Model):
    name = models.CharField(max_length=100, unique=True)
    line = models.CharField(max_length=50)  # 'Blue Line', 'Red Line'
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.line})"

class Review(models.Model):
    ML_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    review_text = models.TextField()
    overall_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    ml_status = models.CharField(max_length=20, choices=ML_STATUS_CHOICES, default='pending')
    helpful_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review for {self.station.name} - {self.overall_rating}/5"

class AspectSentiment(models.Model):
    ASPECT_CHOICES = [
        ('metro_station_infrastructure', 'Metro Station Infrastructure'),
        ('metro_station_connectivity', 'Metro Station Connectivity'),
        ('general_safety', 'General Safety'),
        ('crowd_management', 'Crowd Management'),
        ('metro_frequency', 'Metro Frequency'),
        ('cleanliness', 'Cleanliness'),
        ('womens_safety', 'Women\'s Safety'),
        ('ticketing_system', 'Ticketing System'),
        ('staff_behavior', 'Staff Behavior'),
    ]
    
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ]
    
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='aspects')
    aspect = models.CharField(max_length=30, choices=ASPECT_CHOICES)
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES)
    score = models.DecimalField(max_digits=4, decimal_places=3)
    confidence = models.DecimalField(max_digits=4, decimal_places=3)
    
    class Meta:
        unique_together = ['review', 'aspect']

class StationStats(models.Model):
    station = models.OneToOneField(Station, on_delete=models.CASCADE)
    total_reviews = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    # Rating distribution
    rating_1_count = models.PositiveIntegerField(default=0)
    rating_2_count = models.PositiveIntegerField(default=0)
    rating_3_count = models.PositiveIntegerField(default=0)
    rating_4_count = models.PositiveIntegerField(default=0)
    rating_5_count = models.PositiveIntegerField(default=0)
    
    updated_at = models.DateTimeField(auto_now=True)

class AspectStats(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    aspect = models.CharField(max_length=35)
    
    positive_count = models.PositiveIntegerField(default=0)
    negative_count = models.PositiveIntegerField(default=0)
    neutral_count = models.PositiveIntegerField(default=0)
    satisfaction_percentage = models.PositiveIntegerField(default=0)  # 0-100
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['station', 'aspect']