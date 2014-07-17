from django.contrib import admin
from graphit.models import Link
from graphit.models import Node
from graphit.models import Graph
from graphit.models import AbstractNode
from graphit.models import Color
from graphit.models import Comment

class NodeAdmin(admin.ModelAdmin):
  list_display = ('title', 'getUrl')


# Register your models here.
admin.site.register(Link)
admin.site.register(Node)
admin.site.register(Graph)
admin.site.register(AbstractNode)
admin.site.register(Color)
admin.site.register(Comment)
