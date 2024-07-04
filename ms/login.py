import tkinter as tk
from tkinter import ttk
from admin import AdminApp
from user import UserApp

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        window_width = 400
        window_height = 400

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.root.configure(bg='light blue')
        self.frame = tk.Frame(self.root, bg='light blue')
        self.frame.pack(padx=20, pady=150)
        
        style = ttk.Style(self.root)
        style.theme_use('clam')

        self.root.p1 = tk.PhotoImage(file='login.png')
        self.root.iconphoto(False, self.root.p1)
        
        self.create_ui()

    def admin(self):
        self.root.destroy()
        admin_app = AdminApp(tk.Tk())

    def user(self):
        self.root.destroy()
        user_app = UserApp(tk.Tk())

    def create_ui(self):
        label = tk.Label(self.frame, text="Meeting Scheduler", font=("Georgia", 18, "bold"), bg='light blue')
        label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        admin1 = tk.Button(self.frame, text="Admin", font=("Georgia", 10), command=self.admin)
        user1 = tk.Button(self.frame, text="User", font=("Georgia", 10), command=self.user)
        admin1.grid(row=1, column=0, padx=30)
        user1.grid(row=1, column=1, padx=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
