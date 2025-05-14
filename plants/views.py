from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Plant, Watering, Note
from itertools import chain
from operator import attrgetter
from django.views.generic import DetailView
from .forms import PlantForm
from collections import defaultdict

def dashboard(request):
    group_by = request.session.get('group_by', 'category')  # or 'location'
    plants = Plant.objects.select_related('category', 'location')

    groups = defaultdict(list)
    for plant in plants:
        key_obj = getattr(plant, group_by)
        key = key_obj.name if key_obj else "Uncategorized"
        groups[key].append(plant)

    context = {
        'categories': groups,
        'uncategorized': groups.get("Uncategorized", []),
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
        
        waterings = plant.watering_set.all()
        notes = plant.note_set.all()
        
        # Create timeline with proper field access
        timeline = []
        for watering in waterings:
            timeline.append({
                'type': 'watering',
                'date': watering.date,
                'object': watering
            })
        
        for note in notes:
            timeline.append({
                'type': 'note',
                'date': note.created_at,
                'object': note
            })
        
        # Sort by date descending
        timeline.sort(key=lambda x: x['date'], reverse=True)
        
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

def update_grouping(request):
    if request.method == 'POST':
        group_by = request.POST.get('group_by')
        if group_by in ['category', 'location']:
            request.session['group_by'] = group_by
    return redirect('dashboard')