from node import Node

class AVLTree:
    def __init__(self):
        self.root = None

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