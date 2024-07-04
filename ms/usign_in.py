import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import subprocess

class SigninApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign-In")
        
        window_width = 400
        window_height = 400
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.root.configure(bg='light blue')
        self.frame = tk.Frame(self.root, bg='light blue')
        self.frame.pack(padx=20, pady=100)

        style = ttk.Style(self.root)
        style.theme_use('clam')

        self.root.p1 = tk.PhotoImage(file='sign in.png')
        self.root.iconphoto(False, self.root.p1)
        
        label = tk.Label(self.frame, text="Sign-In", font=("Georgia", 18, "bold"), bg='light blue')
        label.grid(row=0, column=0, columnspan=5, pady=(10, 20))

        self.create_ui()
    
    def validate_input(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="sys", auth_plugin="mysql_native_password")
        cursor = mydb.cursor()

        query = "SELECT * FROM user WHERE username = %s AND password = %s"

        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            self.root.destroy()
            subprocess.run(["python", "pdashboard.py"], shell=True)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def create_ui(self):
        row = 1
        username_label = tk.Label(self.frame, text="Username:", font=("Georgia", 10), bg='light blue')
        username_label.grid(row=row, column=0, sticky='w')
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=row, column=1, sticky='w', pady=10)

        row += 1
        password_label = tk.Label(self.frame, text="Password:", font=("Georgia", 10), bg='light blue')
        password_label.grid(row=row, column=0, sticky='w')
        self.password_entry = tk.Entry(self.frame, show='*')
        self.password_entry.grid(row=row, column=1, sticky='w', pady=10)

        row += 1
        submit_button = tk.Button(self.frame, text="Submit", font=("Georgia", 8), command=self.validate_input, bg='gray65')
        submit_button.grid(row=row, column=0, columnspan=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = SigninApp(root)
    root.mainloop()
