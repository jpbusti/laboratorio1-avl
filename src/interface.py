from PIL import Image
import customtkinter as ctk
from tkinter import messagebox
from .avl_tree import AVLTree
from .node import Node
from .visualizer import visualizer

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Interfaz:
    def __init__(self, tree):
        self.tree = tree
        self.visualizer = visualizer()

        self.root = ctk.CTk()
        self.root.title("Sistema de Cursos - AVL")
        self.root.geometry("900x600")

        # Layout principal
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.root, width=200)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Contenido
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.create_sidebar()
        self.create_main_menu()

    #SIDEBAR
    def create_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="Menú", font=("Arial", 20)).pack(pady=20)

        botones = [
            ("Insertar", self.insert_form),
            ("Eliminar", self.delete_form),
            ("Buscar", self.search_form),
            ("Recorrido", self.show_levels),
            ("Visualizar", self.visualize)
        ]

        for texto, comando in botones:
            ctk.CTkButton(self.sidebar, text=texto, command=comando)\
                .pack(pady=10, padx=10, fill="x")

    #LIMPIAR
    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    #MENÚ PRINCIPAL
    def create_main_menu(self):
        self.clear_main()

        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Menú Principal", font=("Arial", 40)).pack(pady=20)
        ctk.CTkLabel(frame, text="Selecciona una opción del menú lateral").pack(pady=10)

    #INSERTAR
    def insert_form(self):
        self.clear_main()
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(expand=True)
        ctk.CTkLabel(frame, text="Insertar Curso por ID", font=("Arial", 25))\
            .pack(pady=20)
        self.entry_id = ctk.CTkEntry(frame)
        self.entry_id.pack(pady=10)
        ctk.CTkButton(frame, text="Insertar", command=self.insert_node)\
            .pack(pady=10)
        ctk.CTkButton(frame, text="Volver", command=self.create_main_menu)\
            .pack(pady=10)

    def insert_node(self):
        try:
            node_id = int(self.entry_id.get())
            node = self.get_course_by_id(node_id)  #alvaro aqui pon la funcion que busca por id
            if node is None:
                messagebox.showerror("Error", "No se encontró el curso")
                return
            if self.tree.search_by_id(self.tree.root, node_id):
                messagebox.showerror("Error", "El nodo ya existe")
                return
            self.tree.root = self.tree.insert(self.tree.root, node)
            messagebox.showinfo("Éxito", "Curso insertado")
            self.visualize()
        except:
            messagebox.showerror("Error", "ID inválido")

    #ELIMINAR
    def delete_form(self):
        self.clear_main()

        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Eliminar Curso (ID)", font=("Arial", 25)).pack(pady=10)
        self.delete_entry = ctk.CTkEntry(frame)
        self.delete_entry.pack(pady=10)

        ctk.CTkButton(frame, text="Eliminar", command=self.delete_node).pack(pady=10)
        ctk.CTkButton(frame, text="Volver", command=self.create_main_menu).pack(pady=10)

    def delete_node(self):
        try:
            id_val = int(self.delete_entry.get())
            self.tree.root = self.tree.delete(self.tree.root, id_val)
            messagebox.showinfo("Éxito", "Curso eliminado")
            self.visualize()
        except:
            messagebox.showerror("Error", "ID inválido")

    #BUSCAR
    def search_form(self):
        self.clear_main()

        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Buscar Curso (ID)", font=("Arial", 25)).pack(pady=5)
        self.search_entry = ctk.CTkEntry(frame)
        self.search_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="Buscar por satisfacción", font=("Arial", 25)).pack(pady=5)
        self.search_sat_entry = ctk.CTkEntry(frame)
        self.search_sat_entry.pack(pady=5)

        ctk.CTkButton(frame, text="Buscar", command=self.search_node).pack(pady=5)
        ctk.CTkButton(frame, text="Búsqueda por criterios", command=self.search_by_criteria).pack(pady=5)
        ctk.CTkButton(frame, text="Volver", command=self.create_main_menu).pack(pady=5)

    def search_node(self):
        try:
            id_text = self.search_entry.get().strip()
            sat_text = self.search_sat_entry.get().strip()

            if id_text and sat_text:
                messagebox.showerror("Error", "Ingrese solo uno")
                return

            result = None

            if id_text:
                result = self.tree.search_by_id(self.tree.root, int(id_text))
            elif sat_text:
                result = self.tree.search_by_satisfaction(self.tree.root, int(sat_text))
            else:
                messagebox.showerror("Error", "Ingrese un valor")
                return

            if result:
                self.current_node = result
                self.show_node_options()
            else:
                messagebox.showinfo("Resultado", "No encontrado")

        except:
            messagebox.showerror("Error", "Datos inválidos")

    def show_node_options(self):
        self.clear_main()
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        ctk.CTkLabel(frame, text="Nodo encontrado", font=("Arial", 25))\
            .pack(pady=10)
        ctk.CTkLabel(frame, text=f"ID: {self.current_node.course_id}")\
            .pack(pady=5)
        #BOTONES DE OPCIONES
        opciones = [
        ("Ver información completa", self.show_full_info),
        ("Obtener nivel", self.show_level),
        ("Factor de balanceo", self.show_balance),
        ("Padre", self.show_parent),
        ("Abuelo", self.show_grandparent),
        ("Tío", self.show_uncle)
        ]
        for texto, comando in opciones:
            ctk.CTkButton(frame, text=texto, command=comando)\
                .pack(pady=5, fill="x", padx=50)
        # Área de resultados
        self.result_box = ctk.CTkTextbox(frame, height=150)
        self.result_box.pack(fill="both", expand=True, pady=10)
        ctk.CTkButton(frame, text="Volver", command=self.create_main_menu)\
            .pack(pady=10)

    def show_full_info(self):
        n = self.current_node

        info = f"""
        ID: {n.course_id}
    Title: {n.title}
    Rating: {n.rating}
    Satisfaction: {n.satisfaction}
    Num reviews: {n.num_reviews}
    Num published lectures: {n.num_published_lectures}
    Created: {n.created}
    Last update date: {n.last_update_date}
    Duration: {n.duration}
    Instructors ID: {n.instructors_id}
    Image: {n.image}
    Positive reviews: {n.positive_reviews}
    Negative reviews: {n.negative_reviews}
    Neutral reviews: {n.neutral_reviews}
"""
        self.update_result(info)
    
    def show_level(self):
        level = self.tree.get_level(self.tree.root, self.current_node)
        self.update_result(f"Nivel: {level}")

    def show_balance(self):
        balance = self.tree.get_balance(self.current_node)
        self.update_result(f"Factor de balanceo: {balance}")

    def show_parent(self):
        self.update_result("No implementado")

    def show_grandparent(self):
        self.update_result("No implementado")

    def show_uncle(self):
        self.update_result("No implementado")

    def update_result(self, text):
        self.result_box.configure(state="normal")
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", text)
        self.result_box.configure(state="disabled")

    def search_by_criteria(self):
        messagebox.showinfo("Info", "No implementado")

    #RECORRIDO
    def show_levels(self):
        self.clear_main()
        textbox = ctk.CTkTextbox(self.main_frame)
        textbox.pack(fill="both", expand=True, padx=20, pady=20)
        result = self.tree.level_order()  
        recorrido_lineal = []
        textbox.insert("end", "RECORRIDO POR NIVELES\n\n")
        for i, nivel in enumerate(result):
            texto_nivel = " -> ".join(str(n) for n in nivel)
            textbox.insert("end", f"Nivel {i}: {texto_nivel}\n")
            recorrido_lineal.extend(nivel)
        #recorrido completo
        recorrido_str = " -> ".join(str(n) for n in recorrido_lineal)
        textbox.insert("end", "\nRECORRIDO COMPLETO\n\n")
        textbox.insert("end", recorrido_str)
        textbox.configure(state="disabled")

    #VISUALIZAR
    def visualize(self):
        self.visualizer.visualize(self.tree.root)
        self.show_tree_image()

    def show_tree_image(self):
        self.clear_main()

        canvas = ctk.CTkCanvas(self.main_frame)
        canvas.pack(fill="both", expand=True)

        image = Image.open("tree.png")

        max_width = 800
        ratio = max_width / image.width
        new_size = (int(image.width * ratio), int(image.height * ratio))
        image = image.resize(new_size)

        self.tree_img = ctk.CTkImage(light_image=image, size=new_size)

        label = ctk.CTkLabel(canvas, image=self.tree_img, text="")
        label.pack(expand=True)

        ctk.CTkButton(self.main_frame, text="Volver", command=self.create_main_menu)\
            .pack(pady=10)

    def run(self):
        self.root.mainloop()
