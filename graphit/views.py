from django.shortcuts import render
from django.views import generic
from graphit.models import *

# Create your views here.
class IndexView(generic.ListView):
  template_name = 'graphit/index.html'
  context_object_name = 'latest_graphs'
  def get_queryset(self):
    """Return the last five published polls"""
    return Graph.objects.all

class DetailView(generic.DetailView):
  model = Graph
  template_name = 'graphit/detail.html'
