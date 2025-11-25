import tkinter as tk
from tkinter import ttk, messagebox
from models import BaseSandwich, ADICIONALES

class RestaurantGUI:
    def __init__(self, root):
        self.root = root
        root.title("Restaurante - Decorator")

        self.order = []

        frm = ttk.Frame(root, padding=10)
        frm.grid(row=0, column=0, sticky="nsew")

        # PROTEÍNAS
        ttk.Label(frm, text="Proteína:").grid(row=0, column=0)
        proteins = ["Pavo", "Italiano", "Beef", "Veggie", "Atún", "Pollo"]
        self.protein_var = tk.StringVar(value="Pavo")
        ttk.OptionMenu(frm, self.protein_var, proteins[0], *proteins).grid(row=0, column=1)

        # TAMAÑO
        ttk.Label(frm, text="Tamaño:").grid(row=1, column=0)
        self.size_var = tk.IntVar(value=15)
        ttk.Radiobutton(frm, text="15 cm", variable=self.size_var, value=15).grid(row=1, column=1)
        ttk.Radiobutton(frm, text="30 cm", variable=self.size_var, value=30).grid(row=1, column=2)

        # ADICIONALES (Combobox con cantidades)
        ttk.Label(frm, text="Adicionales (Cantidad):").grid(row=2, column=0)

        self.ad_vars = {}
        col = 1

        for name in ADICIONALES.keys():
            ttk.Label(frm, text=name).grid(row=2, column=col)
            var = tk.IntVar(value=0)
            self.ad_vars[name] = var

            qty = ttk.Combobox(
                frm,
                textvariable=var,
                width=4,
                values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            )
            qty.grid(row=3, column=col)
            col += 1

        # BOTONES
        ttk.Button(frm, text="Agregar Sándwich", command=self.add_sandwich).grid(row=4, column=0)
        ttk.Button(frm, text="Ver Orden", command=self.show_order).grid(row=4, column=1)
        ttk.Button(frm, text="Limpiar Orden", command=self.clear_order).grid(row=4, column=2)
        ttk.Button(frm, text="Guardar Bitácora", command=self.save_log).grid(row=4, column=3)

        # CUADRO DE TEXTO
        self.text = tk.Text(root, width=70, height=12)
        self.text.grid(row=1, column=0)

        # TOTAL
        self.total_var = tk.StringVar(value="Total: $0.00")
        ttk.Label(root, textvariable=self.total_var, font=("Arial", 12)).grid(row=2, column=0)

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

