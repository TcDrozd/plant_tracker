from django.db import models
from django.utils import timezone

class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='plant_images/', blank=True, null=True)
    watering_interval = models.PositiveIntegerField(default=7)

    class Meta:
        ordering = ['name']  # Default alphabetical ordering

    def __str__(self):
        return self.name
    
    def last_watered(self):
        watering = self.watering_set.order_by('-date').first()
        return watering.date if watering else None
    
    def days_since_watered(self):
        last = self.last_watered()
        if not last:
            return None
        return (timezone.now().date() - last).days

class Note(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note for {self.plant.name} ({self.created_at.date()})"

class Watering(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.plant.name} watered on {self.date}"

    class Meta:
        ordering = ['-date']