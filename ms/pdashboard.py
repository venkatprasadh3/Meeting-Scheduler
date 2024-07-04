import tkinter as tk
from tkinter import ttk
import subprocess

class DashboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard")
        
        window_width = 500
        window_height = 700
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.configure(bg='light blue')

        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.frame = tk.Frame(self, bg='light blue')
        self.frame.pack(padx=20, pady=150)

        self.p1 = tk.PhotoImage(file='dashboard.png')
        self.iconphoto(False, self.p1)

        self.create_widgets()

    def create_widgets(self):
        self.img = tk.PhotoImage(file='profile_icon.png')
        self.img = self.img.subsample(3)
        self.lbl = tk.Label(self.frame, image=self.img, bg='light blue')
        self.lbl.grid(row=1, column=1, padx=5, pady=5)

        self.heading_label1 = tk.Label(self.frame, text="Meeting Scheduler", font=("Georgia", 18, "bold"), bg='light blue')
        self.heading_label1.grid(row=0, column=0, columnspan=5, pady=(10, 20), sticky="n")

        self.heading_label2 = tk.Label(self.frame, text="Dashboard", font=("Georgia", 15, "bold"), bg='light blue')
        self.heading_label2.grid(row=2, column=0, columnspan=5, pady=(10, 20), sticky="n")

        button_height = 3

        self.search_button = tk.Button(self.frame, text="Search", font=("Georgia", 10), command=self.search_meeting, height=button_height, bg='light blue')
        self.display_button = tk.Button(self.frame, text="Display", font=("Georgia", 10), command=self.display_meetings, height=button_height, bg='light blue')

        self.search_button.grid(row=3, column=0, columnspan=1, padx=20, pady=20, sticky="n")
        self.display_button.grid(row=3, column=2, columnspan=2, padx=20, pady=20, sticky="n")

    def search_meeting(self):
        self.destroy()
        subprocess.run(["python", "psearch.py"], shell=True)

    def display_meetings(self):
        self.destroy()
        subprocess.run(["python", "pdisplay.py"], shell=True)

if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()
