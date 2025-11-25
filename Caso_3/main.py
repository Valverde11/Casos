# main.py
import tkinter as tk
from gui import AnimatedGUI

def run():
    root = tk.Tk()
    app = AnimatedGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run()
