from PIL import Image
import customtkinter as ctk
from tkinter import messagebox
from avl_tree import AVLTree
from node import Node
from visualizer import visualizer
from search import (search_positive_reviews,
                    search_by_date,
                    search_by_lectures_range,
                    search_by_reviews_above_average)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Interfaz:
    def __init__(self, tree, df):
        self.tree         = tree
        self.df           = df
        self.visualizer   = visualizer()
        self.current_node = None

        self.root = ctk.CTk()
        self.root.title("Sistema de Cursos - AVL")
        self.root.geometry("900x600")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.sidebar = ctk.CTkFrame(self.root, width=200)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.create_sidebar()
        self.create_main_menu()

    # ── Buscar curso en el CSV ────────────────────────────────────────

    def get_course_by_id(self, course_id):
        fila = self.df[self.df["id"] == course_id]
        if fila.empty:
            return None
        curso = fila.iloc[0]
        return Node(
            course_id              = int(curso["id"]),
            title                  = curso["title"],
            url                    = curso["url"],
            rating                 = curso["rating"],
            num_reviews            = curso["num_reviews"],
            num_published_lectures = curso["num_published_lectures"],
            created                = curso["created"],
            last_update_date       = curso["last_update_date"],
            duration               = curso["duration"],
            instructors_id         = curso["instructors_id"],
            image                  = curso["image"],
            positive_reviews       = curso["positive_reviews"],
            negative_reviews       = curso["negative_reviews"],
            neutral_reviews        = curso["neutral_reviews"],
        )

    # ── Sidebar ───────────────────────────────────────────────────────

    def create_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="Menú", font=("Arial", 20)).pack(pady=20)
        botones = [
            ("Insertar",   self.insert_form),
            ("Eliminar",   self.delete_form),
            ("Buscar",     self.search_form),
            ("Recorrido",  self.show_levels),
            ("Visualizar", self.visualize),
        ]
        for texto, comando in botones:
            ctk.CTkButton(self.sidebar, text=texto, command=comando)\
                .pack(pady=10, padx=10, fill="x")

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ── Menú principal ────────────────────────────────────────────────

    def create_main_menu(self):
        self.clear_main()
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(expand=True)
        ctk.CTkLabel(frame, text="Menú Principal", font=("Arial", 40)).pack(pady=20)
        ctk.CTkLabel(frame, text="Selecciona una opción del menú lateral").pack(pady=10)

    # ── Insertar ──────────────────────────────────────────────────────

    def insert_form(self):
        self.clear_main()
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(expand=True)
        ctk.CTkLabel(frame, text="Insertar Curso por ID", font=("Arial", 25)).pack(pady=20)
        self.entry_id = ctk.CTkEntry(frame, placeholder_text="ID del curso")
        self.entry_id.pack(pady=10)
        ctk.CTkButton(frame, text="Insertar", command=self.insert_node).pack(pady=10)
        ctk.CTkButton(frame, text="Volver",   command=self.create_main_menu).pack(pady=10)

    def insert_node(self):
        try:
            node_id = int(self.entry_id.get())
            if self.tree.search_by_id(self.tree.root, node_id):
                messagebox.showerror("Error", "El curso ya está en el árbol")
                return
            node = self.get_course_by_id(node_id)
            if node is None:
                messagebox.showerror("Error", "No se encontró el curso en el dataset")
                return
            self.tree.root = self.tree.insert(self.tree.root, node)
            messagebox.showinfo("Éxito", f"Curso '{node.title}' insertado correctamente")
            self.visualize()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    # ── Eliminar ──────────────────────────────────────────────────────

    def delete_form(self):
        self.clear_main()
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(expand=True)
        ctk.CTkLabel(frame, text="Eliminar Curso", font=("Arial", 25)).pack(pady=10)

        ctk.CTkLabel(frame, text="Eliminar por ID:").pack()
        self.delete_id_entry = ctk.CTkEntry(frame, placeholder_text="ID del curso")
        self.delete_id_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="O eliminar por satisfacción:").pack()
        self.delete_sat_entry = ctk.CTkEntry(frame, placeholder_text="Satisfacción")
        self.delete_sat_entry.pack(pady=5)

        ctk.CTkButton(frame, text="Eliminar", command=self.delete_node).pack(pady=10)
        ctk.CTkButton(frame, text="Volver",   command=self.create_main_menu).pack(pady=5)

    def delete_node(self):
        try:
            id_text  = self.delete_id_entry.get().strip()
            sat_text = self.delete_sat_entry.get().strip()

            if id_text and sat_text:
                messagebox.showerror("Error", "Ingrese solo uno: ID o satisfacción")
                return
            if id_text:
                course_id = int(id_text)
                if not self.tree.search_by_id(self.tree.root, course_id):
                    messagebox.showerror("Error", "El curso no está en el árbol")
                    return
                self.tree.delete_course(course_id)
                messagebox.showinfo("Éxito", f"Curso {course_id} eliminado")
            elif sat_text:
                satisfaction = float(sat_text)
                nodo = self.tree.search_by_satisfaction(self.tree.root, satisfaction)
                if nodo is None:
                    messagebox.showerror("Error", "No se encontró curso con esa satisfacción")
                    return
                self.tree.delete_course(nodo.course_id, satisfaction)
                messagebox.showinfo("Éxito", f"Curso eliminado")
            else:
                messagebox.showerror("Error", "Ingrese un valor")
                return
            self.visualize()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    # ── Buscar ────────────────────────────────────────────────────────

    def search_form(self):
        self.clear_main()
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="Buscar por ID:", font=("Arial", 16)).pack(pady=5)
        self.search_id_entry = ctk.CTkEntry(frame, placeholder_text="ID del curso")
        self.search_id_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="Buscar por satisfacción:", font=("Arial", 16)).pack(pady=5)
        self.search_sat_entry = ctk.CTkEntry(frame, placeholder_text="Satisfacción")
        self.search_sat_entry.pack(pady=5)

        ctk.CTkButton(frame, text="Buscar nodo",
                      command=self.search_node).pack(pady=5)
        ctk.CTkButton(frame, text="Búsqueda por criterios",
                      command=self.search_by_criteria).pack(pady=5)
        ctk.CTkButton(frame, text="Volver",
                      command=self.create_main_menu).pack(pady=10)

    def search_node(self):
        try:
            id_text  = self.search_id_entry.get().strip()
            sat_text = self.search_sat_entry.get().strip()

            if id_text and sat_text:
                messagebox.showerror("Error", "Ingrese solo uno")
                return

            result = None
            if id_text:
                result = self.tree.search_by_id(self.tree.root, int(id_text))
            elif sat_text:
                result = self.tree.search_by_satisfaction(self.tree.root, float(sat_text))
            else:
                messagebox.showerror("Error", "Ingrese un valor")
                return

            if result:
                self.current_node = result
                self.show_node_options()
            else:
                messagebox.showinfo("Resultado", "Curso no encontrado")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def show_node_options(self):
        self.clear_main()
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Nodo encontrado", font=("Arial", 25)).pack(pady=10)
        ctk.CTkLabel(frame,
                     text=f"ID: {self.current_node.course_id} | "
                          f"Satisfacción: {self.current_node.satisfaction}").pack(pady=5)

        opciones = [
            ("Ver información completa", self.show_full_info),
            ("Obtener nivel",            self.show_level),
            ("Factor de balanceo",       self.show_balance),
            ("Padre",                    self.show_parent),
            ("Abuelo",                   self.show_grandparent),
            ("Tío",                      self.show_uncle),
        ]
        for texto, comando in opciones:
            ctk.CTkButton(frame, text=texto, command=comando)\
                .pack(pady=4, fill="x", padx=50)

        self.result_box = ctk.CTkTextbox(frame, height=150)
        self.result_box.pack(fill="both", expand=True, pady=10)
        ctk.CTkButton(frame, text="Volver", command=self.create_main_menu).pack(pady=10)

    def show_full_info(self):
        n = self.current_node
        info = (
            f"ID:                   {n.course_id}\n"
            f"Título:               {n.title}\n"
            f"URL:                  {n.url}\n"
            f"Rating:               {n.rating}\n"
            f"Satisfacción:         {n.satisfaction}\n"
            f"Num reseñas:          {n.num_reviews}\n"
            f"Clases publicadas:    {n.num_published_lectures}\n"
            f"Creado:               {n.created}\n"
            f"Última actualización: {n.last_update_date}\n"
            f"Duración:             {n.duration}\n"
            f"ID instructor:        {n.instructors_id}\n"
            f"Imagen:               {n.image}\n"
            f"Reseñas positivas:    {n.positive_reviews}\n"
            f"Reseñas negativas:    {n.negative_reviews}\n"
            f"Reseñas neutrales:    {n.neutral_reviews}\n"
        )
        self.update_result(info)

    def show_level(self):
        level = self.tree.get_level(self.tree.root, self.current_node)
        self.update_result(f"Nivel del nodo: {level}")

    def show_balance(self):
        balance = self.tree.get_balance(self.current_node)
        self.update_result(f"Factor de balanceo: {balance}")

    def show_parent(self):
        parent = self.tree.get_parent(self.tree.root, self.current_node)
        if parent:
            self.update_result(f"Padre → ID: {parent.course_id} | Título: {parent.title}")
        else:
            self.update_result("Este nodo es la raíz, no tiene padre")

    def show_grandparent(self):
        grandparent = self.tree.get_grandparent(self.current_node)
        if grandparent:
            self.update_result(f"Abuelo → ID: {grandparent.course_id} | Título: {grandparent.title}")
        else:
            self.update_result("Este nodo no tiene abuelo")

    def show_uncle(self):
        uncle = self.tree.get_uncle(self.current_node)
        if uncle:
            self.update_result(f"Tío → ID: {uncle.course_id} | Título: {uncle.title}")
        else:
            self.update_result("Este nodo no tiene tío")

    def update_result(self, text):
        self.result_box.configure(state="normal")
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", text)
        self.result_box.configure(state="disabled")

    # ── Búsqueda por criterios ────────────────────────────────────────

    def search_by_criteria(self):
        self.clear_main()
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        ctk.CTkLabel(frame, text="Búsqueda por criterios", font=("Arial", 22)).pack(pady=10)

        criterios = [
            ("A: Positivas > Negativas + Neutrales",
             lambda: self.run_criteria(search_positive_reviews(self.tree.root))),
            ("B: Fecha de creación posterior a...", self.criteria_b_form),
            ("C: Clases en rango...",               self.criteria_c_form),
            ("D: Reseñas sobre el promedio...",     self.criteria_d_form),
        ]
        for texto, comando in criterios:
            ctk.CTkButton(frame, text=texto, command=comando)\
                .pack(pady=6, fill="x", padx=30)
        ctk.CTkButton(frame, text="Volver", command=self.create_main_menu).pack(pady=10)

    def criteria_b_form(self):
        self.clear_main()
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(expand=True)
        ctk.CTkLabel(frame, text="Fecha posterior a (YYYY-MM-DD):").pack(pady=10)
        entry = ctk.CTkEntry(frame, placeholder_text="2020-01-01")
        entry.pack(pady=5)
        ctk.CTkButton(frame, text="Buscar",
                      command=lambda: self.run_criteria(
                          search_by_date(self.tree.root, entry.get().strip())
                      )).pack(pady=10)
        ctk.CTkButton(frame, text="Volver", command=self.search_by_criteria).pack(pady=5)

    def criteria_c_form(self):
        self.clear_main()
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(expand=True)
        ctk.CTkLabel(frame, text="Clases mínimas:").pack(pady=5)
        min_entry = ctk.CTkEntry(frame, placeholder_text="10")
        min_entry.pack(pady=5)
        ctk.CTkLabel(frame, text="Clases máximas:").pack(pady=5)
        max_entry = ctk.CTkEntry(frame, placeholder_text="100")
        max_entry.pack(pady=5)
        ctk.CTkButton(frame, text="Buscar",
                      command=lambda: self.run_criteria(
                          search_by_lectures_range(
                              self.tree.root, int(min_entry.get()), int(max_entry.get())
                          )
                      )).pack(pady=10)
        ctk.CTkButton(frame, text="Volver", command=self.search_by_criteria).pack(pady=5)

    def criteria_d_form(self):
        self.clear_main()
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(expand=True)
        ctk.CTkLabel(frame, text="Tipo de reseña:").pack(pady=10)
        tipo = ctk.CTkOptionMenu(frame, values=["positive", "negative", "neutral"])
        tipo.pack(pady=5)
        ctk.CTkButton(frame, text="Buscar",
                      command=lambda: self.run_criteria(
                          search_by_reviews_above_average(self.tree.root, tipo.get())
                      )).pack(pady=10)
        ctk.CTkButton(frame, text="Volver", command=self.search_by_criteria).pack(pady=5)

    def run_criteria(self, results):
        self.clear_main()
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        ctk.CTkLabel(frame,
                     text=f"Resultados: {len(results)} nodos encontrados",
                     font=("Arial", 18)).pack(pady=10)

        if not results:
            ctk.CTkLabel(frame, text="No se encontraron resultados").pack(pady=20)
        else:
            textbox = ctk.CTkTextbox(frame)
            textbox.pack(fill="both", expand=True, pady=10)
            for node in results:
                textbox.insert("end",
                               f"ID: {node.course_id} | "
                               f"Satisfacción: {node.satisfaction} | "
                               f"Título: {node.title}\n")
            textbox.configure(state="disabled")

            ctk.CTkLabel(frame, text="Ingresa el ID para ver sus opciones:").pack()
            id_entry = ctk.CTkEntry(frame)
            id_entry.pack(pady=5)
            ctk.CTkButton(frame, text="Seleccionar",
                          command=lambda: self.select_node_from_results(
                              int(id_entry.get()), results
                          )).pack(pady=5)

        ctk.CTkButton(frame, text="Volver", command=self.search_by_criteria).pack(pady=10)

    def select_node_from_results(self, course_id, results):
        for node in results:
            if node.course_id == course_id:
                self.current_node = node
                self.show_node_options()
                return
        messagebox.showerror("Error", "ID no encontrado en los resultados")

    # ── Recorrido por niveles ─────────────────────────────────────────

    def show_levels(self):
        self.clear_main()
        textbox = ctk.CTkTextbox(self.main_frame)
        textbox.pack(fill="both", expand=True, padx=20, pady=20)
        result = self.tree.level_order()
        if not result:
            textbox.insert("end", "El árbol está vacío")
        else:
            textbox.insert("end", "RECORRIDO POR NIVELES\n\n")
            recorrido_lineal = []
            for i, nivel in enumerate(result):
                texto_nivel = " -> ".join(str(n) for n in nivel)
                textbox.insert("end", f"Nivel {i}: {texto_nivel}\n")
                recorrido_lineal.extend(nivel)
            recorrido_str = " -> ".join(str(n) for n in recorrido_lineal)
            textbox.insert("end", "\nRECORRIDO COMPLETO\n\n")
            textbox.insert("end", recorrido_str)
        textbox.configure(state="disabled")

    # ── Visualizar árbol ──────────────────────────────────────────────

    def visualize(self):
        self.visualizer.visualize(self.tree.root)
        self.show_tree_image()

    def show_tree_image(self):
        self.clear_main()
        try:
            image = Image.open("tree.png")

            # Tomar el tamaño real del panel
            self.main_frame.update_idletasks()
            panel_w = self.main_frame.winfo_width()  - 40
            panel_h = self.main_frame.winfo_height() - 80

            # Escalar manteniendo proporción
            img_w, img_h = image.size
            ratio = min(panel_w / img_w, panel_h / img_h)
            new_size = (int(img_w * ratio), int(img_h * ratio))
            image = image.resize(new_size, Image.LANCZOS)  # LANCZOS = mejor calidad

            self.tree_img = ctk.CTkImage(light_image=image, size=new_size)
            canvas = ctk.CTkFrame(self.main_frame)
            canvas.pack(fill="both", expand=True)
            ctk.CTkLabel(canvas, image=self.tree_img, text="").pack(expand=True)

        except FileNotFoundError:
            ctk.CTkLabel(self.main_frame,
                        text="El árbol está vacío, inserta nodos primero")\
                .pack(expand=True)

        ctk.CTkButton(self.main_frame, text="Volver",
                    command=self.create_main_menu).pack(pady=10)

    def run(self):
        self.root.mainloop()
