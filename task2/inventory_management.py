import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

# Database Setup
def initialize_db():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    
    # Create users table for authentication
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
    # Create products table for inventory
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Add default user (for testing purposes)
def add_default_user():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    if count == 0:  # If no users exist, add a default user
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
        conn.commit()
    conn.close()

# Authentication
def authenticate_user(username, password):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Main Window
def main_window():
    def load_products():
        for row in tree.get_children():
            tree.delete(row)
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        for row in cursor.fetchall():
            tree.insert("", END, values=row)
        conn.close()

    def add_product():
        name = entry_name.get()
        price = entry_price.get()
        quantity = entry_quantity.get()
        if not name or not price or not quantity:
            messagebox.showerror("Input Error", "All fields are required.")
            return
        try:
            price = float(price)
            quantity = int(quantity)
            conn = sqlite3.connect("inventory.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
            conn.commit()
            conn.close()
            load_products()
            entry_name.delete(0, END)
            entry_price.delete(0, END)
            entry_quantity.delete(0, END)
        except ValueError:
            messagebox.showerror("Input Error", "Price must be a number and quantity must be an integer.")

    def edit_product():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a product to edit.")
            return
        product_id = tree.item(selected_item[0])['values'][0]
        name = entry_name.get()
        price = entry_price.get()
        quantity = entry_quantity.get()
        if not name or not price or not quantity:
            messagebox.showerror("Input Error", "All fields are required.")
            return
        try:
            price = float(price)
            quantity = int(quantity)
            conn = sqlite3.connect("inventory.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE products SET name = ?, price = ?, quantity = ? WHERE id = ?", (name, price, quantity, product_id))
            conn.commit()
            conn.close()
            load_products()
        except ValueError:
            messagebox.showerror("Input Error", "Price must be a number and quantity must be an integer.")

    def delete_product():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a product to delete.")
            return
        product_id = tree.item(selected_item[0])['values'][0]
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()
        load_products()

    def low_stock_alert():
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE quantity < 5")
        low_stock_items = cursor.fetchall()
        conn.close()
        if low_stock_items:
            alert_message = "Low stock items:\n\n"
            for item in low_stock_items:
                alert_message += f"{item[1]} - {item[3]} left\n"
            messagebox.showwarning("Low Stock Alert", alert_message)

    def generate_sales_summary():
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(price * quantity) FROM products")
        total_sales = cursor.fetchone()[0] or 0
        conn.close()
        messagebox.showinfo("Sales Summary", f"Total sales: ${total_sales:.2f}")

    # Main Inventory Window
    root = ttk.Window(themename="darkly")
    root.title("Inventory Management System")

    # Product Form
    frame_form = ttk.Frame(root, padding=10)
    frame_form.pack(fill=X)

    ttk.Label(frame_form, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    entry_name = ttk.Entry(frame_form)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_form, text="Price:").grid(row=1, column=0, padx=5, pady=5)
    entry_price = ttk.Entry(frame_form)
    entry_price.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_form, text="Quantity:").grid(row=2, column=0, padx=5, pady=5)
    entry_quantity = ttk.Entry(frame_form)
    entry_quantity.grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(frame_form, text="Add", command=add_product).grid(row=3, column=0, padx=5, pady=5)
    ttk.Button(frame_form, text="Edit", command=edit_product).grid(row=3, column=1, padx=5, pady=5)
    ttk.Button(frame_form, text="Delete", command=delete_product).grid(row=3, column=2, padx=5, pady=5)
    ttk.Button(frame_form, text="Low Stock Alert", command=low_stock_alert).grid(row=3, column=3, padx=5, pady=5)
    ttk.Button(frame_form, text="Sales Summary", command=generate_sales_summary).grid(row=3, column=4, padx=5, pady=5)

    # Product Table
    frame_table = ttk.Frame(root, padding=10)
    frame_table.pack(fill=BOTH, expand=True)

    columns = ("ID", "Name", "Price", "Quantity")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill=BOTH, expand=True)

    load_products()
    root.mainloop()

# Login Window
def login_window():
    def on_login():
        username = entry_username.get()
        password = entry_password.get()
        if authenticate_user(username, password):
            messagebox.showinfo("Login Success", "Successfully logged in!")
            login_win.destroy()  # Close login window
            main_window()  # Open main inventory window
        else:
            messagebox.showerror("Authentication Error", "Invalid username or password.")

    login_win = ttk.Window(themename="darkly")
    login_win.title("Login")
    login_win.geometry("900x800")
    ttk.Label(login_win, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    entry_username = ttk.Entry(login_win)
    entry_username.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(login_win, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    entry_password = ttk.Entry(login_win, show="*")
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(login_win, text="Login", command=on_login).grid(row=2, columnspan=2, pady=5)
    login_win.mainloop()

if __name__ == "__main__":
    initialize_db()
    add_default_user()  # Add default user if none exists
    login_window()
