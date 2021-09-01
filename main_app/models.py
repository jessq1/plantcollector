from django.db import models
from django.urls import reverse

TIMES = (
  ('M', 'Morning'),
  ('E', 'Evening')
)

# Create your models here.
class Plant(models.Model):
  name = models.CharField(max_length=100)
  origin = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  age = models.IntegerField()

  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
    return reverse('plants_detail', kwargs={'plant_id': self.id})

class Water(models.Model):
  date = models.DateField()
  time = models.CharField(max_length=1,choices=TIMES,default=TIMES[0][0])

  plant= models.ForeignKey(Plant, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.get_time_display()} on {self.date}"
  class Meta:
    ordering = ['-date']