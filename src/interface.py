from PIL import Image
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from avl_tree import AVLTree
from node import Node
from visualizer import visualizer
from search import (search_positive_reviews,
                    search_by_date,
                    search_by_lectures_range,
                    search_by_reviews_above_average)

# Configuración visual general de la app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Interfaz:
    def __init__(self, tree, df):
        # Guarda el árbol AVL y el dataframe
        self.tree = tree
        self.df = df

        # Objeto que genera la imagen del árbol
        self.visualizer = visualizer()

        # Nodo actual seleccionado en búsquedas
        self.current_node = None

        # Ventana principal
        self.root = ctk.CTk()
        self.root.title("Sistema de Cursos - AVL")
        self.root.geometry("1000x650")

        # Configuración del layout
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Panel izquierdo (menú)
        self.sidebar = ctk.CTkFrame(self.root, width=200)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")

        # Encabezado superior
        self.header = ctk.CTkFrame(self.root, height=60)
        self.header.grid(row=0, column=1, sticky="ew")

        # Área principal donde cambia el contenido
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=1, column=1, sticky="nsew")

        # Crear secciones iniciales
        self.create_header()
        self.create_sidebar()
        self.create_main_menu()

    # Crea el título superior
    def create_header(self):
        ctk.CTkLabel(self.header, text="Sistema de Cursos AVL",
                     font=("Arial", 22, "bold")).pack(side="left", padx=20)

    # Crea el menú lateral con botones
    def create_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="Menú", font=("Arial", 20)).pack(pady=20)

        botones = [
            ("Insertar", self.insert_form),
            ("Eliminar", self.delete_form),
            ("Buscar", self.search_form),
            ("Recorrido", self.show_levels),
            ("Visualizar", self.visualize),
        ]

        for texto, comando in botones:
            ctk.CTkButton(self.sidebar, text=texto, command=comando)\
                .pack(pady=10, padx=10, fill="x")

    # Limpia la pantalla antes de mostrar otra sección
    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.content = ctk.CTkFrame(self.main_frame)
        self.content.pack(fill="both", expand=True, padx=40, pady=30)

    # Crea una sección con título
    def create_section(self, title):
        frame = ctk.CTkFrame(self.content)
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text=title,
                     font=("Arial", 28, "bold")).pack(pady=20)

        sub = ctk.CTkFrame(frame)
        sub.pack(pady=10, padx=20)

        return sub

    # ---------- MENÚ ----------
    def create_main_menu(self):
        self.clear_main()

        frame = ctk.CTkFrame(self.content)
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text=" Sistema de Cursos AVL ",
                     font=("Arial", 36, "bold")).pack(pady=20)

        ctk.CTkLabel(frame,
                     text="Gestión de cursos usando árbol AVL",
                     font=("Arial", 16)).pack(pady=10)

        # Muestra cantidad de nodos
        stats = ctk.CTkFrame(frame)
        stats.pack(pady=20)

        total = self.count_nodes(self.tree.root)

        ctk.CTkLabel(stats, text=f"Nodos en árbol: {total}",
                     font=("Arial", 18)).pack(padx=20, pady=10)

    # Busca un curso en el dataframe y crea un nodo
    def get_course_by_id(self, course_id):
        fila = self.df[self.df["id"] == course_id]

        if fila.empty:
            return None

        curso = fila.iloc[0]

        return Node(
            int(curso["id"]),
            curso["title"],
            curso["url"],
            curso["rating"],
            curso["num_reviews"],
            curso["num_published_lectures"],
            curso["created"],
            curso["last_update_date"],
            curso["duration"],
            curso["instructors_id"],
            curso["image"],
            curso["positive_reviews"],
            curso["negative_reviews"],
            curso["neutral_reviews"],
        )

    # ---------- INSERTAR ----------

    def insert_form(self):
        self.clear_main()

        frame = self.create_section("Insertar Curso")

        ctk.CTkLabel(frame, text="Ingrese el ID del curso").pack(pady=5)

        self.entry_id = ctk.CTkEntry(frame, width=250)
        self.entry_id.pack(pady=10)

        ctk.CTkButton(frame, text="Insertar",
                      command=self.insert_node,
                      width=200).pack(pady=10)

    # Inserta un nodo en el árbol
    def insert_node(self):
        try:
            node_id = int(self.entry_id.get())

            # Verifica si ya existe
            if self.tree.search_by_id(self.tree.root, node_id):
                CTkMessagebox(title="Error", message="Ya existe", icon="cancel")
                return

            node = self.get_course_by_id(node_id)

            if node is None:
                CTkMessagebox(title="Error", message="No encontrado", icon="cancel")
                return

            # Inserción AVL
            self.tree.root = self.tree.insert(self.tree.root, node)

            msg = CTkMessagebox(title="Éxito", message="Insertado", icon="check")
            msg.get()
            self.visualize()

        except:
            CTkMessagebox(title="Error", message="Dato inválido", icon="cancel")

    # ---------- ELIMINAR ----------

    def delete_form(self):
        self.clear_main()

        frame = self.create_section("Eliminar Curso")

        ctk.CTkLabel(frame, text="Eliminar por ID").pack()
        self.delete_id_entry = ctk.CTkEntry(frame, width=250)
        self.delete_id_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="O por satisfacción").pack()
        self.delete_sat_entry = ctk.CTkEntry(frame, width=250)
        self.delete_sat_entry.pack(pady=5)

        ctk.CTkButton(frame, text="Eliminar",
                      command=self.delete_node).pack(pady=10)

    # Elimina un nodo según ID o satisfacción
    def delete_node(self):
        try:
            id_text = self.delete_id_entry.get().strip()
            sat_text = self.delete_sat_entry.get().strip()

            if id_text and sat_text:
                CTkMessagebox(title="Error", message="Ingrese solo un criterio", icon="cancel")
                return

            if id_text:
                course_id = int(id_text)

                if not self.tree.search_by_id(self.tree.root, course_id):
                    CTkMessagebox(title="Error", message="ID no encontrado", icon="cancel")
                    return

                self.tree.delete_course(course_id)

            elif sat_text:
                satisfaction = float(sat_text)

                nodo = self.tree.search_by_satisfaction(self.tree.root, satisfaction)

                if nodo is None:
                    CTkMessagebox(title="Error", message="Satisfacción no encontrada", icon="cancel")
                    return

                self.tree.delete_course(nodo.course_id, satisfaction)

            msg =CTkMessagebox(title="Éxito", message="Eliminado", icon="check")
            msg.get()
            self.visualize()

        except:
            CTkMessagebox(title="Error", message="Dato inválido", icon="cancel")

    # ---------- BUSCAR ----------

    def search_form(self):
        self.clear_main()

        frame = self.create_section("Buscar Curso")

        # Entradas básicas
        ctk.CTkLabel(frame, text="Buscar por ID").pack()
        self.search_id_entry = ctk.CTkEntry(frame, width=250)
        self.search_id_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="Buscar por satisfacción").pack()
        self.search_sat_entry = ctk.CTkEntry(frame, width=250)
        self.search_sat_entry.pack(pady=5)

        # Botones de búsqueda
        ctk.CTkButton(frame, text="Buscar nodo",
                      command=self.search_node).pack(pady=10)

        ctk.CTkButton(frame, text="Búsqueda avanzada",
                      command=self.search_by_criteria).pack(pady=5)

        # Opciones avanzadas
        self.criteria_option = ctk.CTkOptionMenu(
            frame,
            values=[
                "Reseñas positivas > negativas + neutras",
                "Cursos después de una fecha",
                "Rango de número de clases",
                "Reseñas por encima del promedio"
            ],
            command=self.update_criteria_inputs
        )
        self.criteria_option.pack(pady=10)

        self.criteria_frame = ctk.CTkFrame(frame)
        self.criteria_frame.pack(pady=10)

    # Cambia inputs según opción elegida
    def update_criteria_inputs(self, option):
        for widget in self.criteria_frame.winfo_children():
            widget.destroy()

        if option == "Cursos después de una fecha":
            ctk.CTkLabel(self.criteria_frame, text="Fecha (YYYY-MM-DD)").pack()
            self.date_entry = ctk.CTkEntry(self.criteria_frame, width=200)
            self.date_entry.pack(pady=5)

        elif option == "Rango de número de clases":
            ctk.CTkLabel(self.criteria_frame, text="Min lecturas").pack()
            self.min_lectures_entry = ctk.CTkEntry(self.criteria_frame, width=200)
            self.min_lectures_entry.pack(pady=5)

            ctk.CTkLabel(self.criteria_frame, text="Max lecturas").pack()
            self.max_lectures_entry = ctk.CTkEntry(self.criteria_frame, width=200)
            self.max_lectures_entry.pack(pady=5)

        elif option == "Reseñas por encima del promedio":
            ctk.CTkLabel(self.criteria_frame, text="Tipo de review").pack()
            self.review_type_option = ctk.CTkOptionMenu(
                self.criteria_frame,
                values=["positive", "negative", "neutral"]
            )
            self.review_type_option.pack(pady=5)

    # Busca un nodo específico
    def search_node(self):
        node_id = self.search_id_entry.get()
        sat = self.search_sat_entry.get()

        node = None

        if node_id:
            try:
                node = self.tree.search_course_by_id(int(node_id))
            except:
                node = None

        elif sat:
            try:
                node = self.tree.search_course_by_satisfaction(float(sat))
            except:
                node = None

        if node:
            self.current_node = node
            self.show_node_options()
        else:
            CTkMessagebox(title="Resultado", message="Nodo no encontrado", icon="info")

    # Muestra opciones del nodo encontrado
    def show_node_options(self):
        self.clear_main()

        frame = ctk.CTkFrame(self.content)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text=f"Curso: {self.current_node.course_id}").pack(pady=10)

        self.result_box = ctk.CTkTextbox(frame, height=120)
        self.result_box.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(frame, text="a. Ver información completa",
                      command=self.show_full_info).pack(pady=5)

        ctk.CTkButton(frame, text="b. Nivel del nodo",
                      command=self.show_level).pack(pady=5)

        ctk.CTkButton(frame, text="c. Factor de balance",
                      command=self.show_balance).pack(pady=5)

        ctk.CTkButton(frame, text="d. Padre",
                      command=self.show_parent).pack(pady=5)

        ctk.CTkButton(frame, text="e. Abuelo",
                      command=self.show_grandparent).pack(pady=5)

        ctk.CTkButton(frame, text="f. Tío",
                      command=self.show_uncle).pack(pady=5)

        ctk.CTkButton(frame, text="Volver",
                      command=self.search_form).pack(pady=10)

    # Muestra información completa del nodo
    def show_full_info(self):
        n = self.current_node

        text = (
            f"ID: {n.course_id}\n"
            f"Satisfacción: {n.satisfaction}\n"
            f"👍 {n.positive_reviews} | 👎 {n.negative_reviews} | 😐 {n.neutral_reviews}\n"
            f"Lectures: {n.num_published_lectures}\n"
            f"Fecha: {n.created}"
        )

        self.show_result(text)

    # Muestra nivel del nodo
    def show_level(self):
        level = self.tree.get_level(self.tree.root, self.current_node)
        self.show_result(f"Nivel del nodo: {level}")

    # Padre del nodo
    def show_parent(self):
        parent = self.tree.get_parent(self.tree.root, self.current_node)

        if parent:
            self.show_result(f"Padre: {parent.course_id}")
        else:
            self.show_result("No tiene padre (es la raíz)")

    # Abuelo
    def show_grandparent(self):
        grandparent = self.tree.get_grandparent(self.current_node)

        if grandparent:
            self.show_result(f"Abuelo: {grandparent.course_id}")
        else:
            self.show_result("No tiene abuelo")

    # Tío
    def show_uncle(self):
        uncle = self.tree.get_uncle(self.current_node)

        if uncle:
            self.show_result(f"Tío: {uncle.course_id}")
        else:
            self.show_result("No tiene tío")

    # Factor de balance del AVL
    def show_balance(self):
        balance = self.tree.get_balance(self.current_node)
        self.show_result(f"Factor de balance: {balance}")

    # Muestra resultados en el textbox
    def show_result(self, text):
        if hasattr(self, "result_box"):
            self.result_box.configure(state="normal")
            self.result_box.delete("1.0", "end")
            self.result_box.insert("end", str(text))
            self.result_box.configure(state="disabled")

    # Búsquedas avanzadas
    def search_by_criteria(self):
        root = self.tree.root
        results = []
        option = self.criteria_option.get()

        if option == "Reseñas positivas > negativas + neutras":
            results = search_positive_reviews(root)

        elif option == "Cursos después de una fecha":
            date = self.date_entry.get()
            results = search_by_date(root, date)

        elif option == "Rango de número de clases":
            min_l = int(self.min_lectures_entry.get())
            max_l = int(self.max_lectures_entry.get())
            results = search_by_lectures_range(root, min_l, max_l)

        elif option == "Reseñas por encima del promedio":
            review_type = self.review_type_option.get()
            results = search_by_reviews_above_average(root, review_type)

        self.show_nodes(results)

    # Muestra lista de nodos encontrados
    def show_nodes(self, nodes):
        for widget in self.content.winfo_children():
            if isinstance(widget, ctk.CTkScrollableFrame):
                widget.destroy()

        frame = ctk.CTkScrollableFrame(self.content, height=300)
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        if not nodes:
            ctk.CTkLabel(frame, text="No hay resultados").pack(pady=10)
            return

        for n in nodes:
            text = f"ID: {n.course_id} | Sat: {n.satisfaction} | Lectures: {n.num_published_lectures}"
            ctk.CTkLabel(frame, text=text, anchor="w").pack(fill="x", padx=10, pady=5)

    # Cuenta nodos
    def count_nodes(self, node):
        if node is None:
            return 0
        return 1 + self.count_nodes(node.left) + self.count_nodes(node.right)

    # ---------- RECORRIDO ----------

    def show_levels(self):
        if self.tree.root is None:
            CTkMessagebox(title="Error", message="el arbol no tiene nodos", icon="cancel")
            return
        self.clear_main()
        frame = ctk.CTkFrame(self.content)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame,
                 text="Recorrido Level Order",
                 font=("Arial", 26, "bold")).pack(pady=10)

        niveles = self.tree.level_order()

        # Convierte niveles a lista lineal
        recorrido = [n for nivel in niveles for n in nivel]

        # Texto tipo: 10 → 15 → 20
        recorrido_text = "  →  ".join(str(n.course_id) for n in recorrido)

        textbox = ctk.CTkTextbox(frame, height=80)
        textbox.pack(fill="x", padx=20, pady=10)
        textbox.insert("end", recorrido_text)
        textbox.configure(state="disabled")

        # Parte visual
        self.recorrido_widgets = []

        container = ctk.CTkFrame(frame)
        container.pack(pady=20)

        for nivel in niveles:
            fila = ctk.CTkFrame(container)
            fila.pack(pady=5)

            for n in nivel:
                label = ctk.CTkLabel(fila,
                                 text=str(n.course_id),
                                 width=60,
                                 height=40,
                                 corner_radius=10)
                label.pack(side="left", padx=5)

                self.recorrido_widgets.append(label)

        # Botones de control
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame,
                  text="▶ Iniciar recorrido",
                  command=lambda: self.animate_step(0)).pack(side="left", padx=10)

        ctk.CTkButton(btn_frame,
                  text="Reiniciar",
                  command=self.reset_animation).pack(side="left", padx=10)

    # Animación paso a paso
    def animate_step(self, index):
        if index > 0:
            self.recorrido_widgets[index - 1].configure(fg_color="blue")

        if index < len(self.recorrido_widgets):
            self.recorrido_widgets[index].configure(fg_color="red")
            self.root.after(600, lambda: self.animate_step(index + 1))

    # Reinicia colores
    def reset_animation(self):
        for widget in self.recorrido_widgets:
            widget.configure(fg_color="gray")

    # ---------- VISUALIZACIÓN ----------

    def visualize(self):
        if self.tree.root is None:
            CTkMessagebox(title="Error", message="el arbol no tiene nodos", icon="cancel")
            return
        self.visualizer.visualize(self.tree.root)
        self.show_tree_image()

    # Muestra imagen del árbol
    def show_tree_image(self):
        self.clear_main()

        try:
            image = Image.open("tree.png")

            container = ctk.CTkFrame(self.content)
            container.pack(fill="both", expand=True, padx=20, pady=20)

            canvas = ctk.CTkCanvas(container)
            canvas.pack(side="left", fill="both", expand=True)

            scrollbar_y = ctk.CTkScrollbar(container, orientation="vertical", command=canvas.yview)
            scrollbar_y.pack(side="right", fill="y")

            scrollbar_x = ctk.CTkScrollbar(self.content, orientation="horizontal", command=canvas.xview)
            scrollbar_x.pack(fill="x")

            canvas.configure(yscrollcommand=scrollbar_y.set,
                             xscrollcommand=scrollbar_x.set)

            inner_frame = ctk.CTkFrame(canvas)
            canvas.create_window((0, 0), window=inner_frame, anchor="nw")

            image.thumbnail((1000, 700))

            img = ctk.CTkImage(light_image=image, size=image.size)

            label = ctk.CTkLabel(inner_frame, image=img, text="")
            label.pack()

            self.tree_img = img

            inner_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

        except:
            ctk.CTkLabel(self.content, text="Error al mostrar árbol").pack(pady=20)

        ctk.CTkButton(self.content, text="Volver",
                      command=self.create_main_menu).pack(pady=10)

    # Ejecuta programa
    def run(self):
        self.root.mainloop()