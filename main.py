import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.avl_tree import AVLTree
from src.interface import Interfaz

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "dataset_courses_with_reviews.csv")

try:
    df = pd.read_csv(CSV_PATH)
    print(f"Dataset cargado: {len(df)} registros")
except FileNotFoundError:
    print(f"ERROR: No se encontró el dataset en {CSV_PATH}")
    print("Asegúrate de poner el CSV en la carpeta 'data/'")
    sys.exit(1)


tree = AVLTree()
app  = Interfaz(tree, df)
app.run()
