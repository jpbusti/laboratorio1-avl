from PIL import Image
import customtkinter as ctk
import customtkinter as ctk
from tkinter import messagebox
from .avl_tree import AVLTree
from .node import Node
from .visualizer import visualizer

ctk.set_appearance_mode("dark")  # 🌙 modo oscuro
ctk.set_default_color_theme("blue")

class Interfaz:
    def __init__(self, tree):
        self.tree = tree
        self.visualizer = visualizer()

        self.root = ctk.CTk()
        self.root.title("Sistema de Cursos - AVL")
        self.root.geometry("500x500")

        self.create_main_menu()

    #MENÚ PRINCIPAL
    def create_main_menu(self):
        ctk.CTkLabel(self.root, text="Menú Principal", font=("Arial", 20)).pack(pady=10)

        ctk.CTkButton(self.root, text="Insertar curso", command=self.insert_form).pack(pady=5)
        ctk.CTkButton(self.root, text="Eliminar curso", command=self.delete_form).pack(pady=5)
        ctk.CTkButton(self.root, text="Buscar curso", command=self.search_form).pack(pady=5)
        ctk.CTkButton(self.root, text="Búsqueda por criterios", command=self.search_by_criteria).pack(pady=5)
        ctk.CTkButton(self.root, text="Recorrido por niveles", command=self.show_levels).pack(pady=5)
        ctk.CTkButton(self.root, text="Visualizar árbol", command=self.visualize).pack(pady=5)

        self.output = ctk.CTkLabel(self.root, text="")
        self.output.pack(pady=10)

    #LIMPIAR
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    #INSERTAR
    def insert_form(self):
        self.clear()

        frame = ctk.CTkFrame(self.root)
        frame.pack(pady=10, padx=10, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Insertar Curso", font=("Arial", 18))\
            .grid(row=0, column=0, columnspan=4, pady=10)
        self.entries = {}
        fields = [
        "id", "titulo", "url", "puntaje", "numero de revisiones",
        "numero de lecciones publicadas", "fecha de creación", "fecha de última actualización",
        "duración", "id de instructores", "imagen",
        "revisiones positivas", "revisiones negativas", "revisiones neutrales"
        ]
        for i, field in enumerate(fields):
            row = i // 2 + 1
            col = (i % 2) * 2
            ctk.CTkLabel(frame, text=field)\
            .grid(row=row, column=col, padx=5, pady=5, sticky="w")
            entry = ctk.CTkEntry(frame, width=180)
            entry.grid(row=row, column=col+1, padx=5, pady=5)
            self.entries[field] = entry
        last_row = (len(fields) // 2) + 2
        ctk.CTkButton(frame, text="Guardar", command=self.insert_node)\
            .grid(row=last_row, column=0, columnspan=2, pady=10)
        ctk.CTkButton(frame, text="Volver", command=self.reset)\
            .grid(row=last_row, column=2, columnspan=2, pady=10)

    def insert_node(self):
        try:
            data = {k: v.get() for k, v in self.entries.items()}

            node = Node(
                int(data["id"]), data["title"], data["url"],
                float(data["rating"]), int(data["num_reviews"]),
                int(data["num_published_lectures"]),
                data["created"], data["last_update_date"],
                data["duration"], data["instructors_id"],
                data["image"],
                int(data["positive_reviews"]),
                int(data["negative_reviews"]),
                int(data["neutral_reviews"])
            )

            self.tree.root = self.tree.insert(self.tree.root, node)
            messagebox.showinfo("Éxito", "Curso insertado")

        except:
            messagebox.showerror("Error", "Datos inválidos")

    #ELIMINAR
    def delete_form(self):
        self.clear()

        ctk.CTkLabel(self.root, text="Eliminar Curso (ID)").pack()
        self.delete_entry = ctk.CTkEntry(self.root)
        self.delete_entry.pack()

        ctk.CTkButton(self.root, text="Eliminar", command=self.delete_node).pack(pady=5)
        ctk.CTkButton(self.root, text="Volver", command=self.reset).pack()

    def delete_node(self):
        try:
            id_val = int(self.delete_entry.get())
            self.tree.root = self.tree.delete(self.tree.root, id_val)
            messagebox.showinfo("Éxito", "Curso eliminado")
        except:
            messagebox.showerror("Error", "ID inválido")

    #BUSCAR
    def search_form(self):
        self.clear()

        ctk.CTkLabel(self.root, text="Buscar Curso (ID)").pack()
        self.search_entry = ctk.CTkEntry(self.root)
        self.search_entry.pack()

        ctk.CTkLabel(self.root, text="Buscar por satisfacción").pack()
        self.search_sat_entry = ctk.CTkEntry(self.root)
        self.search_sat_entry.pack()

        ctk.CTkButton(self.root, text="Buscar", command=self.search_node).pack(pady=5)
        ctk.CTkButton(self.root, text="Volver", command=self.reset).pack()

    def search_node(self):
        try:
            id_text = self.search_entry.get().strip()
            sat_text = self.search_sat_entry.get().strip()

            result = None

            if id_text != "" and sat_text != "":
                messagebox.showerror("Error", "Ingrese solo ID o satisfacción")
                return

            if id_text != "":
                result = self.tree.search_by_id(self.tree.root, int(id_text))

            elif sat_text != "":
                result = self.tree.search_by_satisfaction(self.tree.root, int(sat_text))

            else:
                messagebox.showerror("Error", "Ingrese ID o satisfacción")
                return

            if result:
                messagebox.showinfo(
                    "Resultado",
                    f"""ID: {result.course_id}
Title: {result.title}
Satisfaction: {result.satisfaction}
Rating: {result.rating}"""
                )
                self.visualizer.visualize(result)
            else:
                messagebox.showinfo("Resultado", "No encontrado")

        except:
            messagebox.showerror("Error", "Datos inválidos")

    #CRITERIOS
    def search_by_criteria(self):
        messagebox.showinfo("Resultado", "Not implemented")

    #RECORRIDO
    def show_levels(self):
        result = self.tree.level_order()
        messagebox.showinfo("Recorrido por niveles", result)

    #VISUALIZAR
    def visualize(self):
        self.visualizer.visualize(self.tree.root)
        self.show_tree_image()
        ctk.CTkButton(self.root, text="Volver", command=self.reset).pack()

    def show_tree_image(self):
        from PIL import Image
        self.clear()
        canvas = ctk.CTkCanvas(self.root)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y = ctk.CTkScrollbar(self.root, orientation="vertical", command=canvas.yview)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x = ctk.CTkScrollbar(self.root, orientation="horizontal", command=canvas.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        frame = ctk.CTkFrame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")
        image = Image.open("tree.png")
        self.tree_img = ctk.CTkImage(light_image=image, size=image.size)
        label = ctk.CTkLabel(frame, image=self.tree_img, text="")
        label.pack()
        frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    #VOLVER
    def reset(self):
        self.clear()
        self.create_main_menu()

    def run(self):
        self.root.mainloop()