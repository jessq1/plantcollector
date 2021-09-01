from django.shortcuts import render, redirect
from .models import Plant, Pot
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import WaterForm
from django.views.generic import ListView, DetailView



# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def plants_index(request):
    plants = Plant.objects.all()
    return render(request, 'plants/index.html', { 'plants': plants }) 

def plants_detail(request, plant_id):
  plant = Plant.objects.get(id=plant_id)
  water_form = WaterForm()
  return render(request, 'plants/detail.html', { 
    'plant': plant, 'water_form': water_form })

class PlantCreate(CreateView):
  model = Plant
  fields = '__all__'
  success_url = '/plants/'

class PlantUpdate(UpdateView):
  model = Plant
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['origin', 'description', 'age']

class PlantDelete(DeleteView):
  model = Plant
  success_url = '/plants/'

def add_water(request, plant_id):
  form = WaterForm(request.POST)
  if form.is_valid():
    new_water = form.save(commit=False)
    new_water.plant_id = plant_id
    new_water.save()

  return redirect('plants_detail', plant_id=plant_id)

class PotCreate(CreateView):
  model = Pot
  fields = '__all__'

class PotList(ListView):
  model = Pot

class PotDetail(DetailView):
  model = Pot

class PotUpdate(UpdateView):
  model = Pot
  fields = ['name', 'color']

class PotDelete(DeleteView):
  model = Pot
  success_url = '/pots/'