from graphviz import Digraph
from node import Node

class visualizer:
    def __init__(self):
        self.dot = None

    def add_nodes(self, node):
        if node is None:
            return

        # Etiqueta con ID, título corto y satisfacción
        titulo_corto = node.title[:20] + "..." if len(node.title) > 20 else node.title
        label = f"{node.course_id}\n{titulo_corto}\nSat: {node.satisfaction}"

        self.dot.node(
            str(id(node)),
            label,
            shape    = "box",
            style    = "filled,rounded",
            fillcolor= "#2B6CB0",
            fontcolor= "white",
            fontname = "Helvetica",
            fontsize = "11",
            width    = "2",
            height   = "0.8",
        )

        if node.left:
            self.dot.edge(
                str(id(node)), str(id(node.left)),
                color    = "#63B3ED",
                penwidth = "2"
            )
            self.add_nodes(node.left)

        if node.right:
            self.dot.edge(
                str(id(node)), str(id(node.right)),
                color    = "#63B3ED",
                penwidth = "2"
            )
            self.add_nodes(node.right)

    def visualize(self, root, filename="avl_tree"):
        self.dot = Digraph()

        # Configuración general del grafo
        self.dot.attr(
            bgcolor  = "#1A202C",   # fondo oscuro
            rankdir  = "TB",        # top to bottom
            splines  = "ortho",     # líneas rectas
            nodesep  = "0.5",
            ranksep  = "0.8",
        )

        self.add_nodes(root)

        # dpi alto para mejor calidad
        self.dot.attr(dpi="200")
        self.dot.render("tree", format="png", cleanup=True)