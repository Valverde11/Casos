class CalculatorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Bind buttons and keyboard
        self.view.bind_buttons(self)
        self.view.bind_keyboard(self)
        
        # Initialize display
        self.update_display()
    
    def handle_button_click(self, command):
        try:
            if command.isdigit():
                self.model.append_digit(command)
            elif command == '.':
                self.model.append_decimal()
            elif command in ['+', '-', '*', '/']:
                self.model.set_operator(command)
            elif command == '=':
                self.model.calculate_equals()
            elif command == 'C':
                self.model.clear()
            elif command == 'M+':
                self.model.add_to_memory()
            elif command == 'Avg':
                self.model.calculate_average()
            elif command == 'Bin':
                self.model.convert_to_binary()
            elif command == 'Primo':
                self.model.check_prime()
            elif command == 'Data':
                history = self.model.get_operation_history()
                self.view.show_data_window(history)
            
            self.update_display()
        except Exception as e:
            self.view.show_error(f"Error: {str(e)}")
    
    def handle_key_press(self, event):
        key = event.char
        keys_mapping = {
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            '+': '+', '-': '-', '*': '*', '/': '/', '.': '.',
            '=': '=', '\r': '=',  # Enter key
            'c': 'C', 'C': 'C',
            'm': 'M+', 'M': 'M+',
            'a': 'Avg', 'A': 'Avg',
            'b': 'Bin', 'B': 'Bin',
            'p': 'Primo', 'P': 'Primo',
            'd': 'Data', 'D': 'Data'
        }
        
        if key in keys_mapping:
            self.handle_button_click(keys_mapping[key])
            return "break"  # Prevent default handling
    
    def update_display(self):
        display_text = self.model.get_current_input()
        self.view.set_display(display_text)