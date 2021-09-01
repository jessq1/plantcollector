from django.shortcuts import render
from .models import Plant
from django.views.generic.edit import CreateView, UpdateView, DeleteView


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
  return render(request, 'plants/detail.html', { 'plant': plant })

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
