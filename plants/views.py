from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Plant, Watering, Note
from itertools import chain
from operator import attrgetter
from django.views.generic import DetailView
from .forms import PlantForm

def dashboard(request):
    # Get all plants ordered by name
    plants = Plant.objects.all()
    
    # Group plants by category
    categories = {}
    uncategorized = []
    
    for plant in plants:
        if plant.category:
            if plant.category not in categories:
                categories[plant.category] = []
            categories[plant.category].append(plant)
        else:
            uncategorized.append(plant)
    
    # Sort categories alphabetically
    sorted_categories = dict(sorted(categories.items()))
    
    context = {
        'categories': sorted_categories,
        'uncategorized': uncategorized,
    }
    return render(request, 'plants/dashboard.html', context)

def add_plant(request):
    if request.method == 'POST':
        form = PlantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PlantForm()
    return render(request, 'plants/plant_form.html', {'form': form, 'title': 'Add New Plant'})

def edit_plant(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    if request.method == 'POST':
        form = PlantForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PlantForm(instance=plant)
    return render(request, 'plants/plant_form.html', {'form': form, 'title': 'Edit Plant'})

def delete_plant(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    if request.method == 'POST':
        plant.delete()
        return redirect('dashboard')
    return redirect('dashboard')

class PlantDetailView(DetailView):
    model = Plant
    template_name = 'plants/plant_detail.html'
    context_object_name = 'plant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plant = self.get_object()
        
        # Combine watering and notes into timeline
        waterings = Watering.objects.filter(plant=plant)
        notes = Note.objects.filter(plant=plant)
        timeline = sorted(
            chain(waterings, notes),
            key=attrgetter('date' if hasattr(waterings.first(), 'date') else 'created_at'),
            reverse=True
        )
        
        context.update({
            'timeline': timeline,
            'watering_count': waterings.count(),
            'notes_count': notes.count(),
        })
        return context

@require_POST
def water_plant(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    Watering.objects.create(plant=plant, date=timezone.now())
    return JsonResponse({
        'status': 'success',
        'last_watered': timezone.now().date().isoformat(),
        'days': 0
    })

@require_POST
def water_all(request):
    # Water all plants
    today = timezone.now().date()
    plants = Plant.objects.all()
    for plant in plants:
        Watering.objects.create(plant=plant, date=today)
    return JsonResponse({'status': 'success'})

@require_POST
def water_category(request, category):
    # Water all plants in a category
    today = timezone.now().date()
    plants = Plant.objects.filter(category=category)
    for plant in plants:
        Watering.objects.create(plant=plant, date=today)
    return JsonResponse({'status': 'success'})