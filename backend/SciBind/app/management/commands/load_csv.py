import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import EventModel

class Command(BaseCommand):
    help = 'Load events from a CSV file'
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)
    
    def handle(self, *args, **kwargs):
        if EventModel.objects.exists():
            self.stdout.write(self.style.SUCCESS('Events already loaded'))
        with open(kwargs['csv_file'], 'r') as f:
            reader = csv.DictReader(f)
            with transaction.atomic():
                for row in reader:
                    name, materialtype, division = row['Name'], row['Material Type'], row['Division']
                    EventModel.objects.create(name=name, materialtype=materialtype, division=division)
        self.stdout.write(self.style.SUCCESS('Events loaded successfully'))