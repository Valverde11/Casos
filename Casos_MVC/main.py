import tkinter as tk
from model import CalculatorModel
from view import CalculatorView
from controller import CalculatorController

def main():
    # Create root window
    root = tk.Tk()
    
    # Create MVC components
    model = CalculatorModel()
    view = CalculatorView(root)
    controller = CalculatorController(model, view)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()