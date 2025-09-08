# backend/metro_reviews/management/commands/populate_mock_data.py

from django.core.management.base import BaseCommand
from metro_reviews.models import Station, Review, AspectSentiment
import random


class Command(BaseCommand):
    help = 'Populate mock reviews and aspect sentiments for testing'

    def handle(self, *args, **options):
        stations = Station.objects.all()
        if not stations.exists():
            self.stdout.write(self.style.ERROR("⚠️ No stations found. Run populate_stations first."))
            return

        reviews_created = 0
        aspects_created = 0

        sample_reviews = [
            "Great connectivity and clean station!",
            "Crowded during peak hours but manageable.",
            "Staff was very helpful.",
            "Needs improvement in cleanliness.",
            "Good frequency of trains.",
            "Felt safe even at night.",
            "Ticketing system is smooth.",
        ]

        for station in stations:
            for _ in range(random.randint(2, 5)):  # 2–5 reviews per station
                review_text = random.choice(sample_reviews)
                overall_rating = random.randint(2, 5)

                review = Review.objects.create(
                    station=station,
                    review_text=review_text,
                    overall_rating=overall_rating,
                    ml_status="completed",
                )
                reviews_created += 1

                # Add some aspect sentiments
                aspects_to_pick = random.sample(AspectSentiment.ASPECT_CHOICES, 3)  # pick 3 random aspects
                for aspect, _ in aspects_to_pick:
                    sentiment = random.choice(["positive", "negative", "neutral"])
                    score = round(random.uniform(0.5, 1.0), 2)
                    confidence = round(random.uniform(0.6, 0.99), 2)

                    AspectSentiment.objects.create(
                        review=review,
                        aspect=aspect,
                        sentiment=sentiment,
                        score=score,
                        confidence=confidence,
                    )
                    aspects_created += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Created {reviews_created} reviews and {aspects_created} aspect sentiments."
        ))
