from graphviz import Digraph

class visualizer:
    def __init__(self):
        self.dot = None

    # Obtiene balance del nodo
    def get_balance(self, node):
        if node is None:
            return 0
        left_h = node.left.height if node.left else 0
        right_h = node.right.height if node.right else 0
        return left_h - right_h

    # Obtiene color según balance
    def get_color(self, balance):
        if balance == 0:
            return "#48BB78"
        elif abs(balance) == 1:
            return "#ECC94B"
        else:
            return "#F56565"

    # Añade nodos al árbol
    def add_nodes(self, node):
        if node is None:
            return

        balance = self.get_balance(node)
        color = self.get_color(balance)
        title = node.title[:20] + "..." if len(node.title) > 20 else node.title
        label = f"{node.course_id}\n {title}\nSat: {node.satisfaction}\nFB: {balance}"

        self.dot.node(
            str(id(node)),
            label,
            shape="circle",
            style="filled",
            fillcolor=color,
            fontcolor="black"
        )

        if node.left:
            self.dot.edge(
                str(id(node)),
                str(id(node.left)),
                color="blue",
                label="L"
            )
            self.add_nodes(node.left)

        if node.right:
            self.dot.edge(
                str(id(node)),
                str(id(node.right)),
                color="red",
                label="R"
            )
            self.add_nodes(node.right)

    # Genera imagen del árbol
    def visualize(self, root):
        self.dot = Digraph()

        self.dot.attr(
            rankdir="TB",
            bgcolor="white",
            nodesep="0.8",
            ranksep="1.2",
            size="15,20!"
        )

        if root is not None:
            self.add_nodes(root)

        self.dot.render("tree", format="png", cleanup=True)