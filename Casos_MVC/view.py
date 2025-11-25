import tkinter as tk
from tkinter import ttk, messagebox

class CalculatorView:
    def __init__(self, root):
        self.root = root
        self.root.title(" Calculadora MVC - Python")
        self.root.resizable(False, False)
        self.root.configure(bg='#2C3E50')
        
        # Configurar estilo moderno
        self.setup_styles()
        
        # Variables
        self.display_var = tk.StringVar(value="0")
        
        # Create components
        self.create_widgets()
    
    def setup_styles(self):
        style = ttk.Style()
        
        # Configurar tema
        style.theme_use('clam')
        
        # Colores
        self.colors = {
            'primary': '#3498DB',
            'secondary': '#2ECC71',
            'danger': '#E74C3C',
            'warning': '#F39C12',
            'info': '#9B59B6',
            'dark': '#2C3E50',
            'light': '#ECF0F1',
            'display_bg': '#34495E',
            'display_fg': '#1ABC9C'
        }
        
        # Configurar estilos para botones
        style.configure('Number.TButton', 
                       background=self.colors['light'],
                       foreground='#2C3E50',
                       font=('Arial', 12, 'bold'),
                       borderwidth=1,
                       focuscolor='none')
        
        style.configure('Operation.TButton', 
                       background=self.colors['primary'],
                       foreground='white',
                       font=('Arial', 12, 'bold'),
                       borderwidth=1)
        
        style.configure('Advanced.TButton', 
                       background=self.colors['secondary'],
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       borderwidth=1)
        
        style.configure('Equals.TButton', 
                       background=self.colors['warning'],
                       foreground='white',
                       font=('Arial', 12, 'bold'),
                       borderwidth=1)
        
        style.configure('Clear.TButton', 
                       background=self.colors['danger'],
                       foreground='white',
                       font=('Arial', 12, 'bold'),
                       borderwidth=1)
        
        style.configure('Special.TButton', 
                       background=self.colors['info'],
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       borderwidth=1)
        
        # Efectos hover
        style.map('Number.TButton',
                 background=[('active', '#BDC3C7')])
        
        style.map('Operation.TButton',
                 background=[('active', '#2980B9')])
        
        style.map('Advanced.TButton',
                 background=[('active', '#27AE60')])
        
        style.map('Equals.TButton',
                 background=[('active', '#E67E22')])
        
        style.map('Clear.TButton',
                 background=[('active', '#C0392B')])
        
        style.map('Special.TButton',
                 background=[('active', '#8E44AD')])
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.configure(style='Dark.TFrame')
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text=" CALCULADORA MVC", 
            font=('Arial', 16, 'bold'),
            bg=self.colors['dark'],
            fg=self.colors['light'],
            pady=10
        )
        title_label.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E))
        
        # Display Frame
        display_frame = tk.Frame(main_frame, bg=self.colors['display_bg'], relief='sunken', bd=3)
        display_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.display = tk.Entry(
            display_frame, 
            textvariable=self.display_var,
            font=("Digital-7", 20, 'bold'), 
            justify="right", 
            state="readonly",
            bg=self.colors['display_bg'],
            fg=self.colors['display_fg'],
            insertbackground='white',
            relief='flat',
            bd=0
        )
        self.display.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.colors['dark'])
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Definir botones con sus estilos
        buttons = [
            # Fila 1: Funciones avanzadas
            [
                {'text': "M+", 'style': 'Advanced.TButton', 'row': 0, 'col': 0, 'command': 'M+'},
                {'text': "AVG", 'style': 'Advanced.TButton', 'row': 0, 'col': 1, 'command': 'Avg'},
                {'text': "BIN", 'style': 'Advanced.TButton', 'row': 0, 'col': 2, 'command': 'Bin'},
                {'text': "PRIMO", 'style': 'Advanced.TButton', 'row': 0, 'col': 3, 'command': 'Primo'}
            ],
            # Fila 2: Clear y operaciones
            [
                {'text': "C", 'style': 'Clear.TButton', 'row': 1, 'col': 0, 'command': 'C'},
                {'text': "DATA", 'style': 'Special.TButton', 'row': 1, 'col': 1, 'command': 'Data'},
                {'text': "÷", 'style': 'Operation.TButton', 'row': 1, 'col': 2, 'command': '/'},
                {'text': "×", 'style': 'Operation.TButton', 'row': 1, 'col': 3, 'command': '*'}
            ],
            # Fila 3: Números 7-9 y resta
            [
                {'text': "7", 'style': 'Number.TButton', 'row': 2, 'col': 0, 'command': '7'},
                {'text': "8", 'style': 'Number.TButton', 'row': 2, 'col': 1, 'command': '8'},
                {'text': "9", 'style': 'Number.TButton', 'row': 2, 'col': 2, 'command': '9'},
                {'text': "−", 'style': 'Operation.TButton', 'row': 2, 'col': 3, 'command': '-'}
            ],
            # Fila 4: Números 4-6 y suma
            [
                {'text': "4", 'style': 'Number.TButton', 'row': 3, 'col': 0, 'command': '4'},
                {'text': "5", 'style': 'Number.TButton', 'row': 3, 'col': 1, 'command': '5'},
                {'text': "6", 'style': 'Number.TButton', 'row': 3, 'col': 2, 'command': '6'},
                {'text': "+", 'style': 'Operation.TButton', 'row': 3, 'col': 3, 'command': '+'}
            ],
            # Fila 5: Números 1-3 e igual
            [
                {'text': "1", 'style': 'Number.TButton', 'row': 4, 'col': 0, 'command': '1'},
                {'text': "2", 'style': 'Number.TButton', 'row': 4, 'col': 1, 'command': '2'},
                {'text': "3", 'style': 'Number.TButton', 'row': 4, 'col': 2, 'command': '3'},
                {'text': "=", 'style': 'Equals.TButton', 'row': 4, 'col': 3, 'command': '=', 'rowspan': 2}
            ],
            # Fila 6: 0 y decimal
            [
                {'text': "0", 'style': 'Number.TButton', 'row': 5, 'col': 0, 'command': '0', 'colspan': 2},
                {'text': ".", 'style': 'Number.TButton', 'row': 5, 'col': 2, 'command': '.'}
            ]
        ]
        
        # Crear botones
        self.buttons_dict = {}
        for row in buttons:
            for btn_config in row:
                btn = ttk.Button(
                    button_frame, 
                    text=btn_config['text'],
                    style=btn_config['style']
                )
                
                # Configurar grid
                rowspan = btn_config.get('rowspan', 1)
                colspan = btn_config.get('colspan', 1)
                
                btn.grid(
                    row=btn_config['row'], 
                    column=btn_config['col'],
                    rowspan=rowspan,
                    columnspan=colspan,
                    padx=2, 
                    pady=2, 
                    sticky=(tk.W, tk.E, tk.N, tk.S)
                )
                
                self.buttons_dict[btn_config['command']] = btn
        
        # Configurar pesos de grid para responsive
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
            main_frame.grid_columnconfigure(i, weight=1)
    
    def set_display(self, text):
        self.display_var.set(text)
    
    def get_display(self):
        return self.display_var.get()
    
    def bind_buttons(self, controller):
        # Mapeo de comandos a botones
        command_mapping = {
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            '+': '+', '-': '-', '*': '*', '/': '/', '.': '.',
            '=': '=', 'C': 'C', 'M+': 'M+', 'Avg': 'Avg',
            'Bin': 'Bin', 'Primo': 'Primo', 'Data': 'Data'
        }
        
        for command, button_key in command_mapping.items():
            if button_key in self.buttons_dict:
                self.buttons_dict[button_key].configure(
                    command=lambda cmd=command: controller.handle_button_click(cmd)
                )
    
    def bind_keyboard(self, controller):
        self.display.bind('<Key>', controller.handle_key_press)
        # Make sure the display can receive focus for keyboard events
        self.display.configure(state='normal')
        self.display.bind('<FocusIn>', lambda e: self.display.configure(state='normal'))
        self.display.bind('<FocusOut>', lambda e: self.display.configure(state='readonly'))
        
        # Hacer que la ventana principal también reciba eventos de teclado
        self.root.bind('<Key>', controller.handle_key_press)
    
    def show_data_window(self, history):
        data_window = tk.Toplevel(self.root)
        data_window.title(" Bitácora de Operaciones")
        data_window.geometry("700x500")
        data_window.resizable(True, True)
        data_window.configure(bg=self.colors['dark'])
        
        # Título
        title_label = tk.Label(
            data_window,
            text=" HISTORIAL DE OPERACIONES",
            font=('Arial', 14, 'bold'),
            bg=self.colors['dark'],
            fg=self.colors['light'],
            pady=10
        )
        title_label.pack(fill=tk.X)
        
        # Frame para el contenido
        content_frame = tk.Frame(data_window, bg=self.colors['light'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text area con scrollbar
        text_frame = tk.Frame(content_frame, bg=self.colors['light'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        text_area = tk.Text(
            text_frame, 
            wrap=tk.WORD, 
            font=("Consolas", 10),
            bg='#F8F9FA',
            fg='#2C3E50',
            relief='flat',
            padx=10,
            pady=10
        )
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        
        text_area.insert(tk.END, history)
        text_area.configure(state='disabled')
        
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para botones
        button_frame = tk.Frame(content_frame, bg=self.colors['light'])
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Botón cerrar
        close_btn = ttk.Button(
            button_frame, 
            text=" Cerrar", 
            command=data_window.destroy,
            style='Operation.TButton'
        )
        close_btn.pack(pady=5)
        
        # Botón limpiar bitácora
        clear_btn = ttk.Button(
            button_frame,
            text=" Limpiar Bitácora",
            command=lambda: self.clear_log_file(text_area),
            style='Clear.TButton'
        )
        clear_btn.pack(pady=5)
        
        # Set focus to data window
        data_window.focus_set()
    
    def clear_log_file(self, text_area):
        try:
            with open("Bitacora.txt", "w", encoding="utf-8") as f:
                f.write("")
            text_area.configure(state='normal')
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, "Bitácora limpiada exitosamente.\n")
            text_area.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo limpiar la bitácora: {str(e)}")

    def show_error(self, message):
        messagebox.showerror(" Error", message)
    
    def show_info(self, message):
        messagebox.showinfo("ℹ Información", message)