from django import template

register = template.Library()

#Data structure for arborjs
@register.inclusion_tag('print_node.html', name='print_nodes')
def print_nodes(parent):
  allNodes = set()
  getAllChildrenNodes(parent, allNodes)
  return {'allnodes': allNodes}
  #visited = set()
  #return print_node_r(parent, visited)

@register.inclusion_tag('print_node.html', name='print_node_r')
def print_node_r(parent, visited = set()):
  visited.add(parent)
  children = []
  for n in parent.edges.all():
    if n not in visited:
      children.append(n)
  return {'children':children, 'node':parent, 'visited':visited}

@register.inclusion_tag('print_edge.html', name='print_edge')
def print_edge(parent):
  allNodes = set()

  getAllChildrenNodes(parent, allNodes)

  return {'allnodes': allNodes}

def getAllChildrenNodes(parent, allNodes):
  for n in parent.edges.all():
    if n not in allNodes:
      allNodes.add(n)
      getAllChildrenNodes(n, allNodes)

#Flat printing

@register.inclusion_tag('node.html', name='visit')
def visit(parent):
  visited = set()
  return visit_r(parent, visited)

@register.inclusion_tag('node.html', name='visit_r')
def visit_r(parent, visited = set()):
  visited.add(parent)
  children = []
  for n in parent.edges.all():
    if n not in visited:
      children.append(n)
  return {'children':children, 'parent':parent, 'visited':visited}

@register.inclusion_tag('pretty_print.html', name='pretty_print')
def pretty_print(node):
  return {"node":node}

@register.inclusion_tag('leaf_node.html', name='leaf_node')
def leaf_node(node):
  return {"node":node}

@register.inclusion_tag('branch_node.html', name='branch_node')
def leaf_node(node):
  return {"node":node}
