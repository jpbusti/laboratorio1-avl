from .node import Node

class AVLTree:
    def __init__(self):
        self.root = None

    def get_level(self, root, target, level=0):
        if root is None:
            return -1
        if root == target:
            return level
        left = self.get_level(root.left, target, level+1)
        if left != -1:
            return left
        return self.get_level(root.right, target, level+1)

    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
    
    def rotate_left(self, node):
        new_root = node.right          
        sub_tree = new_root.left          
        new_root.left = node
        node.right = sub_tree
        self.update_height(node)
        self.update_height(new_root)
        return new_root          

    def rotate_right(self, node):
        new_root = node.left
        sub_tree = new_root.right
        new_root.right = node
        node.left = sub_tree
        self.update_height(node)
        self.update_height(new_root)
        return new_root  
        
    def rotate_left_right(self, node):
        node.left = self.rotate_left(node.left)
        return self.rotate_right(node)
    
    def rotate_right_left(self, node):
        node.right = self.rotate_right(node.right)
        return self.rotate_left(node)


    #elegi que el nodo se cree antes de intentar insertarlo y se usa self.root = self.insert(self.root, new_node)
    def insert(self, node, new_node):
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
                return node
        self.update_height(node)
        balance =self.get_balance(node)
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
    
    def get_min_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def delete(self, node, course_id, satisfaction=None):
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
            node.left = self.delete(node.left, course_id)
            node.right = self.delete(node.right, course_id)
            if node.course_id == course_id:
                node = self.remove_node(node)

        if node is None:
            return None

        return self.rebalance(node)
    
    def remove_node(self, node):
        # Caso 1: nodo hoja
        if node.left is None and node.right is None:
            return None

        # Caso 2: un solo hijo
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left

        # Caso 3: dos hijos
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
    
    def rebalance(self, node):
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
    
    def delete_course(self, course_id, satisfaction=None):
        self.root = self.delete(self.root, course_id, satisfaction)
    
    def search_by_satisfaction(self, node, satisfaction):
        if node is None:
            return None
        if satisfaction < node.satisfaction:
            return self.search_by_satisfaction(node.left, satisfaction)
        elif satisfaction > node.satisfaction:
            return self.search_by_satisfaction(node.right, satisfaction)
        else:
            return node
        
    def search_by_id(self, node, course_id):
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


            
    "aaa"

    def height(self, node):
        if node is None:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

    def print_level(self, node, level, list=None):
        if node is None:
            return
        if list is None:
            list = []

        if level == 1:
            list.append(node.course_id)
        elif level > 1:
            self.print_level(node.left, level - 1, list)
            self.print_level(node.right, level - 1, list)
        return list
    
    def level_order(self):
        h = self.height(self.root)
        list = []
        for i in range(1, h + 1):
            list.append(self.print_level(self.root, i))
        return list
