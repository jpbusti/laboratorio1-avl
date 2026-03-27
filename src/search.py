from node import Node
from datetime import datetime

def get_all_nodes(node, result=None):
    """
    Realiza un recorrido In-Order (Izquierda, Raíz, Derecha) de forma recursiva.
    """
    if result is None:
        result = []
    if node is None:
        return result
        
    # Navegación hacia el subárbol izquierdo
    get_all_nodes(node.left, result)
    
    # Procesamiento de la raíz del subárbol actual
    result.append(node)
    
    # Navegación hacia el subárbol derecho
    get_all_nodes(node.right, result)
    
    return result

# ── Criterios de Búsqueda y Filtrado ──────────────────────────────────────────

def search_positive_reviews(root):
    """
    Criterio A: Filtra cursos con tendencia de opinión positiva.
    
    Retorna una lista de nodos donde la cantidad de reseñas positivas es 
    estrictamente mayor a la suma de las negativas y neutrales juntas.
    """
    nodes = get_all_nodes(root)
    return [n for n in nodes
            if n.positive_reviews > (n.negative_reviews + n.neutral_reviews)]

def search_by_date(root, date_str):
    """
    Criterio B: Filtra cursos por fecha de creación.
    
    Convierte la cadena de entrada y el atributo 'created' del nodo a objetos 
    datetime para realizar una comparación lógica de 'mayor que' (creados después de).
    """
    nodes = get_all_nodes(root)
    result = []
    try:
        # Definición del límite temporal
        date_limit = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return [] # Retorna lista vacía si el formato de fecha es incorrecto
        
    for node in nodes:
        try:
            # Se extraen los primeros 10 caracteres para asegurar el formato YYYY-MM-DD
            node_date = datetime.strptime(str(node.created)[:10], "%Y-%m-%d")
            if node_date > date_limit:
                result.append(node)
        except:
            continue
    return result

def search_by_lectures_range(root, min_lectures, max_lectures):
    """
    Criterio C: Filtrado por volumen de contenido (Clases).
    
    Utiliza una comparación de rango inclusivo sobre el atributo 
    num_published_lectures.
    """
    nodes = get_all_nodes(root)
    return [n for n in nodes
            if min_lectures <= n.num_published_lectures <= max_lectures]

def search_by_reviews_above_average(root, review_type):
    """
    Criterio D: Filtrado basado en el promedio global del árbol.
    
    1. Calcula el promedio (mean) de un tipo de reseña en todo el árbol.
    2. Filtra los cursos que superan dicho promedio.
    
    Útil para identificar cursos que destacan estadísticamente sobre el dataset.
    """
    nodes = get_all_nodes(root)
    if not nodes:
        return []
        
    if review_type == "positive":
        # Cálculo del promedio global de positivas
        avg = sum(n.positive_reviews for n in nodes) / len(nodes)
        return [n for n in nodes if n.positive_reviews > avg]
        
    elif review_type == "negative":
        # Cálculo del promedio global de negativas
        avg = sum(n.negative_reviews for n in nodes) / len(nodes)
        return [n for n in nodes if n.negative_reviews > avg]
        
    return []