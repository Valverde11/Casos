import tkinter as tk
from tkinter import ttk, messagebox
from models import BaseSandwich, ADICIONALES

class RestaurantGUI:
    def __init__(self, root):
        self.root = root
        root.title("SUBGÜEY - Decorator")
        root.configure(bg="#00FF0D")
        self.order = []

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("My.TFrame", background="#00FF0D")
        style.configure(
            "My.TLabel", 
            background="#00FF0D")
        style.configure(
            "My.TRadiobutton",
            background="#00FF0D",      # color de fondo
            indicatorcolor="#FFFFFF",  # color del circulito
            foreground="black",         # color del texto
            relief="solid",
            borderwidth=0
        )
        style.configure(
            "My.TButton",
            background="#FBFF00",
            foreground="black",
            borderwidth=2,
            bordercolor = "#126900",
        )
        style.configure(
            "My.TMenubutton",
            background="#00B109",
            foreground="black",
            relief="solid",
            borderwidth=2,
            bordercolor = "#126900"
        )
        
        style.configure(
            "My.TCombobox",
            foreground="white",          # color del texto (número)
            background="#00A808",        # fondo general
            fieldbackground="#00A808",   # fondo del campo donde se ve el número
            selectforeground="white",    # color cuando está seleccionado
            selectbackground="#007F00"   # fondo cuando está seleccionado
        )

        style.map(
            "My.TCombobox",
            fieldbackground=[("readonly", "#FFFFFF"), ("!disabled", "#FFFFFF")],
            background=[("active", "#FFFFFF"), ("!disabled", "#FFFFFF")],
            foreground=[("!disabled", "black")],

            # flecha verde
            arrowcolor=[("active", "#00FF00"), ("!disabled", "#00FF00")],
        )
        frm = ttk.Frame(root, padding=10, style="My.TFrame")
        frm.grid(row=0, column=0, sticky="nsew")

        
        
        # PROTEÍNAS
        ttk.Label(frm, text="Proteína:", style="My.TLabel").grid(row=0, column=0)
        proteins = ["Pavo", "Italiano", "Beef", "Veggie", "Atún", "Pollo"]
        self.protein_var = tk.StringVar(value="Pavo")
        self.option = ttk.OptionMenu(frm, self.protein_var, proteins[0], *proteins, style="My.TMenubutton")
        self.option.grid(row=0, column=1)

        menu = self.option["menu"]
        menu.configure(
            bg="#00B109",
            fg="black",
            activebackground="#009600",
            activeforeground="black",
            borderwidth=2,
            relief="solid",
        )


        # TAMAÑO
        ttk.Label(frm, text="Tamaño:", style="My.TLabel").grid(row=1, column=0)
        self.size_var = tk.IntVar(value=15)
        ttk.Radiobutton(frm, text="15 cm", variable=self.size_var, value=15, style="My.TRadiobutton").grid(row=1, column=1)
        ttk.Radiobutton(frm, text="30 cm", variable=self.size_var, value=30, style="My.TRadiobutton").grid(row=1, column=2)

        # ADICIONALES (Combobox con cantidades)
        ttk.Label(frm, text="Adicionales (Cantidad):", style="My.TLabel").grid(row=2, column=0)

        self.ad_vars = {}
        col = 1

        for name in ADICIONALES.keys():
            ttk.Label(frm, text=name, style="My.TLabel").grid(row=2, column=col)
            var = tk.IntVar(value=0)
            self.ad_vars[name] = var

            qty = ttk.Combobox(
                frm,
                textvariable=var,
                width=4,
                values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                style = "My.TCombobox"
            )
            qty.grid(row=3, column=col)
            col += 1

        # BOTONES
        ttk.Button(frm, text="Agregar Sándwich", command=self.add_sandwich, style="My.TButton").grid(row=4, column=0)
        ttk.Button(frm, text="Ver Orden", command=self.show_order, style="My.TButton").grid(row=4, column=1)
        ttk.Button(frm, text="Limpiar Orden", command=self.clear_order, style="My.TButton").grid(row=4, column=4)
        ttk.Button(frm, text="Guardar Bitácora", command=self.save_log, style="My.TButton").grid(row=4, column=6)

        # CUADRO DE TEXTO
        self.text = tk.Text(root, width=70, height=12, bg = "#70EB7B")
        self.text.grid(row=1, column=0)

        # TOTAL
        self.total_var = tk.StringVar(value="Total: $0.00")
        ttk.Label(root, textvariable=self.total_var, font=("Arial", 12), style= "My.TLabel").grid(row=2, column=0)

    def add_sandwich(self):
        s = BaseSandwich(self.protein_var.get(), self.size_var.get())

        # Aplicar adicionales múltiples
        for name, qty in self.ad_vars.items():
            for _ in range(qty.get()):
                s = ADICIONALES[name](s)

        self.order.append((s.description(), s.price()))
        self.update_text()

        messagebox.showinfo("Agregado", "Sándwich añadido.")

    def update_text(self):
        self.text.delete("1.0", tk.END)
        total = 0

        for d, p in self.order:
            self.text.insert(tk.END, f"{d} - ${p:.2f}\n")
            total += p

        self.total_var.set(f"Total: ${total:.2f}")

    def show_order(self):
        self.update_text()

    def clear_order(self):
        self.order = []
        self.update_text()

    def save_log(self):
        with open("bitacora_restaurante.txt", "a", encoding="utf-8") as f:
            for d, p in self.order:
                f.write(f"{d} - ${p:.2f}\n")

        messagebox.showinfo("Guardado", "Bitácora guardada.")

