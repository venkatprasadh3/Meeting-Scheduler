import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import subprocess

class SignupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign-Up")

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

        self.root.p1 = tk.PhotoImage(file='sign up.png')
        self.root.iconphoto(False, self.root.p1)
        
        label = tk.Label(self.frame, text="Sign-Up", font=("Georgia", 18, "bold"), bg='light blue')
        label.grid(row=0, column=0, columnspan=5, pady=(10, 20))

        self.create_ui()

    def validate_input(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="sys", auth_plugin="mysql_native_password")
        cursor = mydb.cursor()
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS user (
            username VARCHAR(255) PRIMARY KEY,
            password VARCHAR(255) NOT NULL
        );
        """
        cursor.execute(create_table_sql)
        mydb.commit()
        query = "INSERT INTO user VALUES (%s, %s)"
        try:
            cursor.execute(query, (username, password))
            mydb.commit()
            mydb.close()
            self.root.destroy()
            subprocess.run(["python", "usign_in.py"], shell=True)
        except mysql.connector.IntegrityError as e:
            messagebox.showerror("Error", "Username already exists.")

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
    app = SignupApp(root)
    root.mainloop()
