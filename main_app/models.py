from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

TIMES = (
  ('M', 'Morning'),
  ('E', 'Evening')
)

# Create your models here.
class Pot(models.Model):
  material = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.material

  def get_absolute_url(self):
    return reverse('pots_detail', kwargs={'pk': self.id})

class Plant(models.Model):
  name = models.CharField(max_length=100)
  origin = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  age = models.IntegerField()
  pots = models.ManyToManyField(Pot)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
    return reverse('plants_detail', kwargs={'plant_id': self.id})

  def watered_for_today(self):
    return self.water_set.filter(date=date.today()).count() >= len(TIMES)

class Water(models.Model):
  date = models.DateField()
  time = models.CharField(max_length=1,choices=TIMES,default=TIMES[0][0])

  plant= models.ForeignKey(Plant, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.get_time_display()} on {self.date}"
  class Meta:
    ordering = ['-date']

class Photo(models.Model):
  url = models.CharField(max_length=250)
  plant = models.OneToOneField(Plant, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for plant_id: {self.plant_id} @{self.url}"