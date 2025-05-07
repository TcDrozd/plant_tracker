from django.contrib import admin
from .models import Plant, Watering

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'created_date')
    list_filter = ('category',)
    search_fields = ('name', 'location', 'category')

@admin.register(Watering)
class WateringAdmin(admin.ModelAdmin):
    list_display = ('plant', 'date')
    list_filter = ('date', 'plant')