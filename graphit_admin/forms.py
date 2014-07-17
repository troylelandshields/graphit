from django import forms
from graphit.models import Graph

class CreateGraphForm(forms.ModelForm):
    class Meta:
        model = Graph
