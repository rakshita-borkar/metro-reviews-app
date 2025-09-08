# management/commands/populate_stations.py

from django.core.management.base import BaseCommand
from metro_reviews.models import Station  

class Command(BaseCommand):
    help = 'Populate database with Mumbai Metro stations'

    def handle(self, *args, **options):
        stations_data = [
            # Blue Line (Line 1)
            {'name': 'Versova', 'line': 'Blue Line'},
            {'name': 'D N Nagar', 'line': 'Blue Line'},
            {'name': 'Azad Nagar', 'line': 'Blue Line'},
            {'name': 'Andheri', 'line': 'Blue Line'},
            {'name': 'Western Express Highway', 'line': 'Blue Line'},
            {'name': 'Chakala', 'line': 'Blue Line'},
            {'name': 'Airport Road', 'line': 'Blue Line'},
            {'name': 'Marol Naka', 'line': 'Blue Line'},
            {'name': 'Saki Naka', 'line': 'Blue Line'},
            {'name': 'Asalpha', 'line': 'Blue Line'},
            {'name': 'Jagruti Nagar', 'line': 'Blue Line'},
            {'name': 'Ghatkopar', 'line': 'Blue Line'},
            
            # Red Line (Line 7)
            {'name': 'Andheri East', 'line': 'Red Line'},
            {'name': 'JB Nagar', 'line': 'Red Line'},
            {'name': 'Marol Naka Red', 'line': 'Red Line'},
            {'name': 'Airport Road Red', 'line': 'Red Line'},
            {'name': 'CSMIA Terminal 1', 'line': 'Red Line'},
            {'name': 'CSMIA Terminal 2', 'line': 'Red Line'},
            
            # Green Line (Line 2A)
            {'name': 'Dahisar East', 'line': 'Green Line'},
            {'name': 'Anand Nagar', 'line': 'Green Line'},
            {'name': 'Eksar', 'line': 'Green Line'},
            {'name': 'Borivali East', 'line': 'Green Line'},
            {'name': 'Magathane', 'line': 'Green Line'},
            {'name': 'National Park', 'line': 'Green Line'},
            
            # Gold Line (Line 2B)
            {'name': 'Andheri West', 'line': 'Gold Line'},
            {'name': 'Kandivali East', 'line': 'Gold Line'},
            {'name': 'Thakur Village', 'line': 'Gold Line'},
        ]

        created_count = 0
        for station_data in stations_data:
            station, created = Station.objects.get_or_create(
                name=station_data['name'],
                defaults={'line': station_data['line']}
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created station: {station.name}")

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} stations. Total stations: {Station.objects.count()}'
            )
        )
