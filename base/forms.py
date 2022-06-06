from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
from .models import Roomy

class RoomForm(ModelForm):
    class Meta:
        model = Roomy
        fields = '__all__'
        exclude = ['host','participants']