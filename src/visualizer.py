from graphviz import Digraph
from .node import Node

class visualizer:
    def __init__(self):
        self.dot = Digraph()
        self.dot.attr('node', shape='circle')   

    def add_nodes(self, node):
        if node is None:
            return    
        # etiqueta del nodo
        label = f"{node.course_id}\nSat: {node.satisfaction}"  
        self.dot.node(str(id(node)), label)
        # hijo izquierdo
        if node.left:
            self.dot.edge(str(id(node)), str(id(node.left)))
            self.add_nodes(node.left)   
        # hijo derecho
        if node.right:
            self.dot.edge(str(id(node)), str(id(node.right)))
            self.add_nodes(node.right)

    def visualize(self, root, filename="avl_tree"):
        self.dot = Digraph()
        self.add_nodes(root)
        self.dot.render("tree", format="png", cleanup=True)