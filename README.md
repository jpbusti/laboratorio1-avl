# Sistema de Cursos AVL

Este proyecto es una aplicación para gestionar cursos usando un árbol AVL. Tiene interfaz gráfica y permite insertar, eliminar, buscar y visualizar los cursos.

## Instalación

Una vez dentro del Codespace, abre la terminal y corre esto:

### Instalar Graphviz

```
sudo apt-get install graphviz
```

### Instalar las librerías de Python

```
pip install pillow customtkinter CTkMessagebox pandas graphviz
```

## ¿Cómo se corre?

```
python main.py
```

## ¿Qué hace cada botón?

**Insertar** → le pones el ID de un curso y lo agrega al árbol

**Eliminar** → le pones el ID o la satisfacción y lo borra del árbol

**Buscar** → busca un curso y te dice cosas como su nivel en el árbol, su padre, su abuelo, etc.

**Recorrido** → muestra todos los nodos del árbol nivel por nivel con una animación

**Visualizar** → genera una imagen del árbol. Los nodos cambian de color según qué tan balanceado está:
- Verde = bien balanceado
- Amarillo = más o menos
- Rojo = desbalanceado

## Errores comunes

**Si dice que no encuentra una librería:**
Vuelve a correr el comando de pip de arriba.

**Si el árbol no se dibuja:**
Asegúrate de haber instalado Graphviz con el comando de apt-get.
