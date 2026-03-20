from .node import Node

def get_all_nodes(node, result=None):
    if result is None:
        result = []
    if node is None:
        return result
    
    get_all_nodes(node.left, result)   
    result.append(node)                
    get_all_nodes(node.right, result)  
    
    return result