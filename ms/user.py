import tkinter as tk
from tkinter import ttk
import subprocess

class UserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User")
        
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

        self.root.p1 = tk.PhotoImage(file='user.png')
        self.root.iconphoto(False, self.root.p1)
        self.create_ui()

    def sign_up(self):
        self.root.destroy()
        subprocess.run(["python", "usign_up.py"], shell=True)

    def sign_in(self):
        self.root.destroy()
        subprocess.run(["python", "usign_in.py"], shell=True)

    def create_ui(self):
        label = tk.Label(self.frame, text="User", font=("Georgia", 18, "bold"), bg='light blue')
        label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        sign_up_button = tk.Button(self.frame, text="Sign-Up", font=("Georgia", 10), command=self.sign_up)
        sign_in_button = tk.Button(self.frame, text="Sign-In", font=("Georgia", 10), command=self.sign_in)
        sign_up_button.grid(row=1, column=0, padx=30)
        sign_in_button.grid(row=1, column=1, padx=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = UserApp(root)
    root.mainloop()
