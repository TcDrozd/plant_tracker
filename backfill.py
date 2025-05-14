import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "plant_tracker.settings")  # adjust if your settings file is elsewhere
django.setup()

from plants.models import Plant, Category, Location

for plant in Plant.objects.all():
    if plant.category_str:
        category_obj, _ = Category.objects.get_or_create(name=plant.category_str.strip())
        plant.category = category_obj

    if plant.location_str:
        location_obj, _ = Location.objects.get_or_create(name=plant.location_str.strip())
        plant.location = location_obj

    plant.save()
