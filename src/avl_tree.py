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

    def insert(self, node, id):
        if node is None:
            return Node(id)
        if id < node.course_id:
            node.left = self.insert(node.left, id)
        elif id > node.course_id:
            node.right = self.insert(node.right, id)
        else:
            print("Error: Course ID already exists")
            return node
        self.update_height(node)
        balance =self.get_balance(node)
        if balance == 2 and self.get_balance(node.left) == 1:
            return self.rotate_right(node)
        elif balance == -2 and self.get_balance(node.right) == -1:
            return self.rotate_left(node)
        if balance == 2 and self.get_balance(node.left) == -1:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        elif balance == -2 and self.get_balance(node.right) == 1:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node
        
        

    
