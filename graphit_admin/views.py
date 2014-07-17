from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from graphit.models import *
from forms import CreateGraphForm

# Create your views here.

def new(request):
  if request.method == 'POST':
    form = CreateGraphForm(request.POST, request.FILES)
    if form.is_valid():
      graph = Graph.create(request.POST['title'], request.FILES['zipped'])

      graph.save()

      return HttpResponseRedirect(reverse('graphit.detail', args=(graph.id,),))
  else:
    form = CreateGraphForm()

  data = {'form': form}
  return render_to_response('graphit_admin/index.html', data, context_instance=RequestContext(request))
