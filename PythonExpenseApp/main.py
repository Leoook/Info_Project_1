import tkinter as tk
from gui.expense_gui import ExpenseGUI

def main():
    root = tk.Tk()
    app = ExpenseGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()