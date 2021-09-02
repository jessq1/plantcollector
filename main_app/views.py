from django.shortcuts import render, redirect
from .models import Plant, Pot, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import WaterForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'plant-collector'

# Create your views here.
class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

@login_required
def plants_index(request):
    plants = Plant.objects.all()
    return render(request, 'plants/index.html', { 'plants': plants }) 

@login_required
def plants_detail(request, plant_id):
  plant = Plant.objects.get(id=plant_id)
  pots_plant_doesnt_have = Pot.objects.exclude(id__in = plant.pots.all().values_list('id'))
  water_form = WaterForm()
  return render(request, 'plants/detail.html', { 
    'plant': plant, 'water_form': water_form, 'pots': pots_plant_doesnt_have })

class PlantCreate(LoginRequiredMixin, CreateView):
  model = Plant
  fields = ['name', 'origin', 'description', 'age']
  success_url = '/plants/'

  def form_valid(self, form):
    form.instance.user = self.request.user 
    return super().form_valid(form)

class PlantUpdate(LoginRequiredMixin, UpdateView):
  model = Plant
  # Let's disallow the renaming of a plant by excluding the name field!
  fields = ['origin', 'description', 'age']

class PlantDelete(LoginRequiredMixin, DeleteView):
  model = Plant
  success_url = '/plants/'

@login_required
def add_water(request, plant_id):
  form = WaterForm(request.POST)
  if form.is_valid():
    new_water = form.save(commit=False)
    new_water.plant_id = plant_id
    new_water.save()

  return redirect('plants_detail', plant_id=plant_id)

class PotCreate(LoginRequiredMixin, CreateView):
  model = Pot
  fields = '__all__'

class PotList(LoginRequiredMixin, ListView):
  model = Pot

class PotDetail(LoginRequiredMixin, DetailView):
  model = Pot

class PotUpdate(LoginRequiredMixin, UpdateView):
  model = Pot
  fields = ['name', 'color']

class PotDelete(LoginRequiredMixin, DeleteView):
  model = Pot
  success_url = '/pots/'

@login_required
def assoc_pot(request, plant_id, pot_id):
  # Note that you can pass a toy's id instead of the whole object
  Plant.objects.get(id=plant_id).pots.add(pot_id)
  return redirect('plants_detail', plant_id=plant_id)

@login_required
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

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('plants_index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)