from gui import MechanismGUI
import tkinter as tk

def main():
    root = tk.Tk()
    root.resizable(False, False)
    app = MechanismGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()