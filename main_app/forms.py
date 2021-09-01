from django.forms import ModelForm
from .models import Water

class WaterForm(ModelForm):
  class Meta:
    model = Water
    fields = ['date', 'time']
