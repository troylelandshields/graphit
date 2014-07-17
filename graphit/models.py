from django.db import models
from zipreader import fileiterator
from django.core.files import File
import shutil
import random
import os

accepted = [".jpg", ".jpeg", ".bmp", ".html", ".pdf", ".png"]

def traverse(zipfile, graph):
  fileiterator(zipfile)
  for root, directories, files in os.walk("temp"):
    for directory in directories:
      if "MACOSX" in root or "MACOSX" in directory:
        continue

      absPath = os.path.join(root, directory)
      parent = os.path.basename(os.path.normpath(os.path.dirname(os.path.dirname(os.path.join(absPath, os.pardir)))))
      if parent in "temp":
        n = Node.create(directory, "root", None, None, graph)
        graph.root = n
        graph.save()
      else:
        parentNode = Node.objects.get(title=parent, graph=graph)
        inside = os.listdir(absPath)
        leaf = True
        links = []
        for i in inside:
          if os.path.isdir(os.path.join(absPath, i)):
            leaf = False
          else:
            fileName, fileExtension = os.path.splitext(os.path.join(absPath, i))
            if(fileExtension.lower() in accepted):
              leaf = True
              l = Link.create("", "soft", os.path.join(absPath, i))
              l.save()
              links.append(l)
        if leaf:
          n = Node.create(directory, "leaf", links, parentNode, graph)
        else:
          n = Node.create(directory, "branch", None, parentNode, graph)
      n.save()
  shutil.rmtree("temp")

class Color(models.Model):
  code = models.CharField(max_length=7)
  name = models.CharField(max_length=20, blank=True)

  def __unicode__(self):
    return self.name + " " + self.code

class AbstractNode(models.Model):
  shape_choices = (('dot', 'Dot'), ('rectangle', 'Rectangle'))

  n_type = models.CharField(max_length=20)
  color = models.ManyToManyField(Color, blank=False)
  shape = models.CharField(max_length=15, choices = shape_choices, default = 'dot')
  alpha = models.FloatField(default=1.0)

  def getColorCode(self):
    count = self.color.count()
    random_index = random.randint(0, count - 1)
    return self.color.all()[random_index].code

  def __unicode__(self):
    return self.n_type

class Link(models.Model):
  type_choices = (('soft', 'Soft'), ('hard', 'Hard'))

  title = models.CharField(max_length=50, blank=True)
  link_type = models.CharField(max_length=15, choices=type_choices, default='soft')
  endpoint = models.FileField(upload_to="graphit_media/files", blank=True)

  def __unicode__(self):
    if self.title:
      return self.title
    else:
      return self.endpoint.url

  @classmethod
  def create(cls, title, link_type, endpoint_path):
    f = open(endpoint_path)
    endpoint = File(f)
    link = cls(title=title, link_type=link_type, endpoint=endpoint)
    return link

class Comment(models.Model):
  link = models.ForeignKey(Link)
  author_display = models.CharField(max_length=100)
  author_email = models.CharField(max_length=200)
  text=models.CharField(max_length=300)

class Node(models.Model):
  shape_choices = (('dot', 'Dot'), ('rectangle', 'Rectangle'))

  title = models.CharField(max_length=50)
  color = models.ManyToManyField(Color, blank=True)
  shape = models.CharField(max_length=15, choices = shape_choices, default = 'dot')
  links = models.ManyToManyField(Link, blank=True)
  edges = models.ManyToManyField('self', blank=True)
  graph = models.ForeignKey('Graph')
  alpha = models.FloatField(default=1.0)
  node_type = models.ForeignKey(AbstractNode)
  use_abstract = models.BooleanField(default=True)
  visited = False

  def __unicode__(self):
    return self.title

  def getColor(self):
    if(self.use_abstract):
      return self.node_type.getColorCode()
    else:
      return self.getColorCode()

  def getColorCode(self):
        count = self.color.count
        random_index = random.randint(0, count - 1)
        return self.color.all()[random_index].code

  def getAlpha(self):
    if(self.use_abstract):
      return self.node_type.alpha
    else:
      return self.alpha

  def getShape(self):
    if(self.use_abstract):
      return self.node_type.shape
    else:
      return self.shape

  def isLinks(self):
    if self.links:
      return True
    else:
      return False

  def getLinksStr(self):
    linkStr = ''
    for idx,link in enumerate(self.links.all()):
      if(idx > 0):
        linkStr += ';'
      linkStr += link.endpoint.url
    return linkStr

  @classmethod
  def create(cls, title, n_type, links, edge, graph):
    node = cls(title=title, graph = graph)
    if(n_type == "leaf" and not links):
      n_type = "linkless_leaf"
    node.node_type = AbstractNode.objects.get(n_type=n_type)
    node.save()

    if (n_type == "leaf"):
      for l in links:
        node.links.add(l)
    if(edge):
      node.edges.add(edge)

    return node


class Graph(models.Model):
  root = models.ForeignKey(Node, related_name='root', null=True, blank=True)
  title = models.CharField(max_length=50)
  zipped = models.FileField(upload_to="static/graphit/zipped", blank=True)

  def __unicode__(self):
    return self.title

  @classmethod
  def create(cls, title, zipped):
    graph = cls(title=title, zipped=zipped)
    graph.save()
    traverse(zipped, graph)

    return graph

if __name__ == '__main__':
  traverse("test.zip")
