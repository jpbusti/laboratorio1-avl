from src.node import Node
from src.avl_tree import AVLTree
from src.interface import Interfaz

tree = AVLTree()

tree.root = tree.insert(tree.root, Node(1, "Título 1", "url", 9, 10, 5, 0, 0, 0, 0, "image", 0, 0, 0))
tree.root = tree.insert(tree.root, Node(2, "Título 2", "url", 4, 10, 5, 0, 0, 0, 0, "image", 0, 0, 0))
tree.root = tree.insert(tree.root, Node(3, "Título 3", "url", 7, 10, 5, 0, 0, 0, 0, "image", 0, 0, 0))
tree.root = tree.insert(tree.root, Node(4, "Título 4", "url", 4, 10, 5, 0, 0, 0, 0, "image", 0, 0, 0))
tree.root = tree.insert(tree.root, Node(5, "Título 5", "url", 2, 10, 5, 0, 0, 0, 0, "image", 0, 0, 0))
tree.root = tree.insert(tree.root, Node(6, "Título 6", "url", 78, 10, 5, 0, 0, 0, 0, "image", 0, 0, 0))
tree.root = tree.insert(tree.root, Node(7, "Título 7", "url", 6 , 10, 5, 0, 0, 0, 0, "image", 0, 0, 0))
tree.root = tree.insert(tree.root, Node(8, "Título 8", "url", 10, 10, 5, 0, 0, 0, 0, "image", 0, 0, 0))
tree.root = tree.insert(tree.root, Node(9, "Título 9", "url", 11, 10, 5, 0, 0, 0, 0, "image", 0, 0, 0))
tree.root = tree.insert(tree.root, Node(10, "Título 10", "url", 12, 10, 5, 0, 0, 0, 0, "image", 0, 0, 0))
tree.root = tree.insert(tree.root, Node(11, "Título 11", "url", 22, 10, 5, 0, 0, 0, 0, "image", 0, 0, 0))
tree.root = tree.insert(tree.root, Node(12, "Título 12", "url", 32, 10, 5, 0, 0, 0, 0, "image", 0, 0, 0))
tree.root = tree.insert(tree.root, Node(13, "Título 13", "url", 42, 10, 5, 0, 0, 0, 0, "image", 0, 0, 0))
tree.root = tree.insert(tree.root, Node(14, "Título 14", "url", 52, 10, 5, 0, 0, 0, 0, "image", 0, 0, 0))
tree.root = tree.insert(tree.root, Node(15, "Título 15", "url", 62, 10, 5, 0, 0, 0, 0, "image", 0, 0, 0))

app = Interfaz(tree)


app.run()