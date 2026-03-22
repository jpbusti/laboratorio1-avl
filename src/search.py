from node import Node
from datetime import datetime

def get_all_nodes(node, result=None):
    if result is None:
        result = []
    if node is None:
        return result
    get_all_nodes(node.left, result)
    result.append(node)
    get_all_nodes(node.right, result)
    return result

# ── Criterio A ────────────────────────────────────────────────────────────────

def search_positive_reviews(root):
    nodes  = get_all_nodes(root)
    return [n for n in nodes
            if n.positive_reviews > (n.negative_reviews + n.neutral_reviews)]

# ── Criterio B ────────────────────────────────────────────────────────────────

def search_by_date(root, date_str):
    nodes  = get_all_nodes(root)
    result = []
    try:
        date_limit = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Formato inválido. Use YYYY-MM-DD")
        return []
    for node in nodes:
        try:
            node_date = datetime.strptime(str(node.created)[:10], "%Y-%m-%d")
            if node_date > date_limit:
                result.append(node)
        except:
            pass
    return result

# ── Criterio C ────────────────────────────────────────────────────────────────

def search_by_lectures_range(root, min_lectures, max_lectures):
    nodes = get_all_nodes(root)
    return [n for n in nodes
            if min_lectures <= n.num_published_lectures <= max_lectures]

# ── Criterio D ────────────────────────────────────────────────────────────────

def search_by_reviews_above_average(root, review_type):
    nodes = get_all_nodes(root)
    if not nodes:
        return []
    if review_type == "positive":
        avg = sum(n.positive_reviews for n in nodes) / len(nodes)
        return [n for n in nodes if n.positive_reviews > avg]
    elif review_type == "negative":
        avg = sum(n.negative_reviews for n in nodes) / len(nodes)
        return [n for n in nodes if n.negative_reviews > avg]
    elif review_type == "neutral":
        avg = sum(n.neutral_reviews for n in nodes) / len(nodes)
        return [n for n in nodes if n.neutral_reviews > avg]
    else:
        print("Tipo inválido. Use: positive, negative o neutral")
        return []
