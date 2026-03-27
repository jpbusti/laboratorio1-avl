from node import Node
from collections import deque

class AVLTree:
    def __init__(self):
        self.root = None

    # ── Altura y balance ──────────────────────────────────────────────

    def get_height(self, node):
        """Retorna la altura del nodo. Si es nulo, la altura es 0."""
        if node is None:
            return 0
        return node.height

    def get_balance(self, node):
        """Calcula el factor de equilibrio (FB = Altura_Izquierda - Altura_Derecha)."""
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        """Recalcula la altura de un nodo tras una rotación o inserción."""
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    # ── Rotaciones ────────────────────────────────────────────────────

    def rotate_left(self, node):
        """Rotación simple a la izquierda (Caso Derecha-Derecha)."""
        new_root = node.right
        sub_tree = new_root.left
        new_root.left = node
        node.right = sub_tree
        self.update_height(node)
        self.update_height(new_root)
        return new_root

    def rotate_right(self, node):
        """Rotación simple a la derecha (Caso Izquierda-Izquierda)."""
        new_root = node.left
        sub_tree = new_root.right
        new_root.right = node
        node.left = sub_tree
        self.update_height(node)
        self.update_height(new_root)
        return new_root

    def rotate_left_right(self, node):
        """Realiza una rotación doble Izquierda-Derecha."""
        node.left = self.rotate_left(node.left)
        return self.rotate_right(node)

    def rotate_right_left(self, node):
        """Realiza una rotación doble Derecha-Izquierda."""
        node.right = self.rotate_right(node.right)
        return self.rotate_left(node)

    # ── Rebalanceo ────────────────────────────────────────────────────

    def rebalance(self, node):
        """Identifica el tipo de desbalance y aplica la rotación correspondiente."""
        self.update_height(node)
        balance = self.get_balance(node)
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)
        if balance > 1 and self.get_balance(node.left) < 0:
            return self.rotate_left_right(node)
        if balance < -1 and self.get_balance(node.right) > 0:
            return self.rotate_right_left(node)
        return node

    # ── Inserción ─────────────────────────────────────────────────────

    def insert(self, node, new_node):
        """Inserta un nodo y rebalancea el camino de regreso a la raíz."""
        if node is None:
            return new_node
        if new_node.satisfaction < node.satisfaction:
            node.left = self.insert(node.left, new_node)
        elif new_node.satisfaction > node.satisfaction:
            node.right = self.insert(node.right, new_node)
        else:
            if new_node.course_id < node.course_id:
                node.left = self.insert(node.left, new_node)
            elif new_node.course_id > node.course_id:
                node.right = self.insert(node.right, new_node)
            else:
                return node  # duplicado, no insertar
        self.update_height(node)
        balance = self.get_balance(node)
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def insert_course(self, new_node):
        """Punto de entrada público para insertar un curso."""
        self.root = self.insert(self.root, new_node)

    # ── Eliminación ───────────────────────────────────────────────────

    def get_min_node(self, node):
        """Encuentra el nodo con la menor satisfacción (el más a la izquierda)."""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def remove_node(self, node):
        """
        Lógica interna para eliminar un nodo específico manejando sus hijos.
        """
        if node.left is None and node.right is None:
            return None
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        sucesor = self.get_min_node(node.right)
        node.course_id              = sucesor.course_id
        node.title                  = sucesor.title
        node.satisfaction           = sucesor.satisfaction
        node.rating                 = sucesor.rating
        node.num_reviews            = sucesor.num_reviews
        node.num_published_lectures = sucesor.num_published_lectures
        node.created                = sucesor.created
        node.last_update_date       = sucesor.last_update_date
        node.duration               = sucesor.duration
        node.instructors_id         = sucesor.instructors_id
        node.image                  = sucesor.image
        node.positive_reviews       = sucesor.positive_reviews
        node.negative_reviews       = sucesor.negative_reviews
        node.neutral_reviews        = sucesor.neutral_reviews
        node.right = self.delete(node.right, sucesor.course_id, sucesor.satisfaction)
        return node

    def delete(self, node, course_id, satisfaction=None):
        """
        Busca y elimina un nodo por satisfacción e ID de forma recursiva.
        Asegura que el árbol permanezca balanceado tras la eliminación.
        """
        if node is None:
            return None
        if satisfaction is not None:
            if satisfaction < node.satisfaction:
                node.left = self.delete(node.left, course_id, satisfaction)
            elif satisfaction > node.satisfaction:
                node.right = self.delete(node.right, course_id, satisfaction)
            else:
                if course_id < node.course_id:
                    node.left = self.delete(node.left, course_id, satisfaction)
                elif course_id > node.course_id:
                    node.right = self.delete(node.right, course_id, satisfaction)
                else:
                    node = self.remove_node(node)
        else:
            node.left  = self.delete(node.left, course_id)
            node.right = self.delete(node.right, course_id)
            if node.course_id == course_id:
                node = self.remove_node(node)
        if node is None:
            return None
        return self.rebalance(node)

    def delete_course(self, course_id, satisfaction=None):
        """Punto de entrada público para eliminar un curso."""
        self.root = self.delete(self.root, course_id, satisfaction)

    # ── Búsqueda simple ───────────────────────────────────────────────

    def search_by_satisfaction(self, node, satisfaction):
        """Busca un nodo por su métrica de satisfacción."""
        if node is None:
            return None
        if satisfaction < node.satisfaction:
            return self.search_by_satisfaction(node.left, satisfaction)
        elif satisfaction > node.satisfaction:
            return self.search_by_satisfaction(node.right, satisfaction)
        else:
            return node

    def search_by_id(self, node, course_id):
        """
        Busca un nodo por su ID. 
        """
        if node is None:
            return None
        if node.course_id == course_id:
            return node
        r = self.search_by_id(node.left, course_id)
        if r is not None:
            return r
        return self.search_by_id(node.right, course_id)

    def search_course_by_id(self, course_id):
        return self.search_by_id(self.root, course_id)

    def search_course_by_satisfaction(self, satisfaction):
        return self.search_by_satisfaction(self.root, satisfaction)

    # ── Nivel, padre, abuelo, tío (recursivos) ────────────────────────

    def get_level(self, root, target, level=0):
        """Calcula recursivamente la profundidad de un nodo en el árbol."""
        if root is None:
            return -1
        if root == target:
            return level
        left = self.get_level(root.left, target, level + 1)
        if left != -1:
            return left
        return self.get_level(root.right, target, level + 1)

    def get_parent(self, root, target, parent=None):
        """Encuentra recursivamente el nodo padre del nodo objetivo."""
        if root is None:
            return None
        if root == target:
            return parent
        left = self.get_parent(root.left, target, root)
        if left is not None:
            return left
        return self.get_parent(root.right, target, root)

    def get_grandparent(self, target):
        """Utiliza el método get_parent dos veces para hallar al abuelo."""
        parent = self.get_parent(self.root, target)
        if parent is None:
            return None
        return self.get_parent(self.root, parent)

    def get_uncle(self, target):
        """Halla al hermano del padre del nodo objetivo."""
        parent = self.get_parent(self.root, target)
        if parent is None:
            return None
        grandparent = self.get_parent(self.root, parent)
        if grandparent is None:
            return None
        if grandparent.left == parent:
            return grandparent.right
        else:
            return grandparent.left

    # ── Recorrido por niveles (recursivo) ─────────────────────────────

    def height(self, node):
        """Calcula la altura real (para el recorrido por niveles)."""
        if node is None:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

    def print_level(self, node, level, result=None):
        """
        Función auxiliar recursiva que añade a una lista todos los nodos
        que se encuentran en un nivel específico.
        """
        if result is None:
            result = []
        if node is None:
            return result
        if level == 1:
            result.append(node)
        elif level > 1:
            self.print_level(node.left,  level - 1, result)
            self.print_level(node.right, level - 1, result)
        return result

    def level_order(self):
        """
        Ejecuta un recorrido Breadth-First Search (BFS) de forma recursiva
        nivel por nivel.
        """
        h = self.height(self.root)
        result = []
        for i in range(1, h + 1):
            result.append(self.print_level(self.root, i))
        return result
