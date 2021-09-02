from django.shortcuts import render, redirect
from .models import Plant, Pot, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import WaterForm
from django.views.generic import ListView, DetailView
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'plant-collector'

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
  pots_plant_doesnt_have = Pot.objects.exclude(id__in = plant.pots.all().values_list('id'))
  water_form = WaterForm()
  return render(request, 'plants/detail.html', { 
    'plant': plant, 'water_form': water_form, 'pots': pots_plant_doesnt_have })

class PlantCreate(CreateView):
  model = Plant
  fields = ['name', 'origin', 'description', 'age']
  success_url = '/plants/'

class PlantUpdate(UpdateView):
  model = Plant
  # Let's disallow the renaming of a plant by excluding the name field!
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

def assoc_pot(request, plant_id, pot_id):
  # Note that you can pass a toy's id instead of the whole object
  Plant.objects.get(id=plant_id).pots.add(pot_id)
  return redirect('plants_detail', plant_id=plant_id)

def add_photo(request, plant_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, plant_id=plant_id)
      plant_photo = Photo.objects.filter(plant_id=plant_id)
      if plant_photo.first():
        plant_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('plants_detail', plant_id=plant_id)
