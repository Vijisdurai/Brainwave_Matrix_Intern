import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
''' 
PIN : 
1234 - user1
6200 - user2
'''
class ATMInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank of Python - ATM")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        self.accounts = {
            '1234': {'name': 'Vijis Durai R', 'account_no': '000123456789', 'balance': 1000.0, 'transactions': []},
            '6200': {'name': 'Vinish Raj', 'account_no': '000987654321', 'balance': 500.0, 'transactions': []}
        }
        self.active_account = None
        self.load_logo()
        self.show_login_screen()

    def load_logo(self):
        try:
            self.logo_image = Image.open("atm.jpg")
            self.logo_image = self.logo_image.resize((100, 100))
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        except Exception:
            self.logo_photo = None

    def show_login_screen(self):
        self.clear_screen()
        if self.logo_photo:
            tk.Label(self.root, image=self.logo_photo, bg='#f0f0f0').pack(pady=10)
        tk.Label(self.root, text="Welcome to Bank of Python", font=("Helvetica", 18, "bold"), bg='#f0f0f0').pack(pady=5)
        tk.Label(self.root, text="Enter PIN:", font=("Helvetica", 12), bg='#f0f0f0').pack(pady=5)
        self.pin_entry = tk.Entry(self.root, show='*', font=("Helvetica", 12), width=20)
        self.pin_entry.pack(pady=5)
        tk.Button(self.root, text="Login", command=self.login, font=("Helvetica", 12), width=15, bg="#4CAF50", fg="white").pack(pady=10)

    def login(self):
        pin = self.pin_entry.get().strip()
        if pin in self.accounts:
            self.active_account = pin
            messagebox.showinfo("Login", "Login Successful!")
            self.show_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid PIN.")

    def show_main_menu(self):
        self.clear_screen()
        account = self.accounts[self.active_account]
        tk.Label(self.root, text=f"Account Holder: {account['name']}", font=("Helvetica", 14), bg='#f0f0f0').pack(pady=5)
        tk.Label(self.root, text=f"Account No: {account['account_no']}", font=("Helvetica", 14), bg='#f0f0f0').pack(pady=5)
        frame = tk.Frame(self.root, bg="#e6e6e6", bd=2, relief=tk.RIDGE)
        frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        buttons = [
            ("Check Balance", self.check_balance_window),
            ("Deposit", self.deposit_window),
            ("Withdraw", self.withdraw_window),
            ("Transaction History", self.transactions_window)
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(frame, text=text, command=command, font=("Helvetica", 12), width=20, height=2, bg="#2196F3", fg="white").grid(row=i // 2, column=i % 2, padx=10, pady=10)
        tk.Button(self.root, text="Logout", command=self.root.quit, font=("Helvetica", 12), width=15, bg="#f44336", fg="white").pack(pady=10)

    def check_balance_window(self):
        self.new_window("Balance", f"Your balance is ${self.accounts[self.active_account]['balance']:.2f}")

    def deposit_window(self):
        self.transaction_window("Deposit", "Enter amount to deposit:", self.deposit_funds)

    def withdraw_window(self):
        self.transaction_window("Withdraw", "Enter amount to withdraw:", self.withdraw_funds)

    def transactions_window(self):
        transactions = self.accounts[self.active_account]['transactions']
        history = "\n".join(transactions) if transactions else "No transactions yet."
        self.new_window("Transaction History", history)

    def transaction_window(self, title, prompt, action):
        new_window = tk.Toplevel()
        new_window.title(title)
        new_window.geometry("400x300")
        new_window.configure(bg='#f0f0f0')
        tk.Label(new_window, text=prompt, font=("Helvetica", 12), bg='#f0f0f0').pack(pady=20)
        amount_entry = tk.Entry(new_window, font=("Helvetica", 12))
        amount_entry.pack(pady=10)
        tk.Button(new_window, text=title, command=lambda: action(amount_entry, new_window), font=("Helvetica", 12), width=15, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(new_window, text="Previous", command=new_window.destroy, font=("Helvetica", 12), width=15, bg="#f44336", fg="white").pack(pady=10)

    def deposit_funds(self, entry, window):
        try:
            amount = float(entry.get())
            if amount > 0:
                self.accounts[self.active_account]['balance'] += amount
                self.accounts[self.active_account]['transactions'].append(f"Deposited ${amount:.2f}")
                messagebox.showinfo("Deposit", f"Deposited ${amount:.2f}")
                window.destroy()
            else:
                messagebox.showerror("Error", "Invalid amount entered.")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount.")

    def withdraw_funds(self, entry, window):
        try:
            amount = float(entry.get())
            balance = self.accounts[self.active_account]['balance']
            if 0 < amount <= balance:
                self.accounts[self.active_account]['balance'] -= amount
                self.accounts[self.active_account]['transactions'].append(f"Withdrew ${amount:.2f}")
                messagebox.showinfo("Withdraw", f"Withdrew ${amount:.2f}")
                window.destroy()
            else:
                messagebox.showerror("Error", "Invalid amount or insufficient funds.")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount.")

    def new_window(self, title, content):
        new_window = tk.Toplevel()
        new_window.title(title)
        new_window.geometry("400x300")
        tk.Label(new_window, text=content, font=("Helvetica", 12), bg='#f0f0f0').pack(pady=50)
        tk.Button(new_window, text="Previous", command=new_window.destroy, font=("Helvetica", 12), width=15, bg="#f44336", fg="white").pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    window = tk.Tk()
    atm_gui = ATMInterface(window)
    window.mainloop()
