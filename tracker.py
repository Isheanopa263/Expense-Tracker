import tkinter as tk
from tkinter import messagebox

def save_data():
    with open("expenses.txt", "w", encoding="utf-8") as f:
        for item in listbox.get(0, tk.END):
            f.write(item + "\n")


def update_total():
    total = 0.0
    for item in listbox.get(0, tk.END):
        try:
            if ' - ₹' in item:
                amt = float(item.split(' - ₹')[1])
                total -= amt
            elif ' + ₹' in item:
                amt = float(item.split(' + ₹')[1])
                total += amt
        except (IndexError, ValueError):
            continue
    total_label.config(text=f"Total: ₹{total:.2f}")

def load_data():
    try:
        with open("expenses.txt", "r", encoding="utf-8") as f:
            for line in f:
                listbox.insert(tk.END, line.strip())
        update_total()
    except FileNotFoundError:
        pass


def add_expense():
    desc = entry_desc.get().strip()
    amt = entry_amt.get().strip()

    if not desc or not amt:
        messagebox.showwarning("Input Required", "Please enter both description and amount.")
        return

    try:
        val = float(amt)
        if val <= 0:
            raise ValueError

        listbox.insert(tk.END, f"- | {desc} >>>>> ₹{val:.2f}")
        entry_desc.delete(0, tk.END)
        entry_amt.delete(0, tk.END)

        update_total()
        save_data()
        messagebox.showinfo("Success", "Expense added successfully.")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid positive amount.")


def delete_expense():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Error", "Please select an expense to delete.")
        return

    listbox.delete(selected[0])
    update_total()
    save_data()
    messagebox.showinfo("Success", "Expense deleted successfully.")

# add an income feature
def add_income():
    desc = entry_desc.get().strip()
    amt = entry_amt.get().strip()

    if not desc or not amt:
        messagebox.showwarning("Input Required", "Please enter both description and amount.")
        return

    try:
        val = float(amt)
        if val <= 0:
            raise ValueError

        listbox.insert(tk.END, f"+ | {desc} >>>>> ₹{val:.2f}")
        entry_desc.delete(0, tk.END)
        entry_amt.delete(0, tk.END)

        update_total()
        save_data()
        messagebox.showinfo("Success", "Income added successfully.")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid positive amount.")


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("400x500")

tk.Label(root, text="Expense Tracker",
         font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Description:").pack(pady=5)
entry_desc = tk.Entry(root)
entry_desc.pack(pady=10)

tk.Label(root, text="Amount:").pack(pady=5)
entry_amt = tk.Entry(root)
entry_amt.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

tk.Button(button_frame, text="Add Expense",
          command=add_expense).pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="Delete",
          command=delete_expense).pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="Exit",
          command=root.quit).pack(side=tk.LEFT, padx=5)

tk.Button(button_frame, text="Add Income",
          command=add_income).pack(side=tk.LEFT, padx=5)

listbox = tk.Listbox(root)
listbox.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

total_label = tk.Label(root, text="Total: ₹0.00",
                       font=("Times New Roman", 14))
total_label.pack(pady=10)

root.bind('<Return>', lambda event: add_expense())

load_data()
root.mainloop()
