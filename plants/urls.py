from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('plant/add/', views.add_plant, name='add_plant'),
    path('plant/<int:pk>/edit/', views.edit_plant, name='edit_plant'),
    path('plant/<int:pk>/delete/', views.delete_plant, name='delete_plant'),
    path('plant/<int:pk>/water/', views.water_plant, name='water_plant'),
    path('water/all/', views.water_all, name='water_all'),
    path('water/category/<str:category>/', views.water_category, name='water_category'),
    path('plant/<int:pk>/', views.PlantDetailView.as_view(), name='plant_detail'),

]