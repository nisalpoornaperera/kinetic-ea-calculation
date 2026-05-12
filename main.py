from gui import KineticsGUI
import tkinter as tk

def main():
    root = tk.Tk()
    root.resizable(False, False)
    app = KineticsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
