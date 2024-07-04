import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
import subprocess

class DeleteMeetingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Delete Meeting")
        
        window_width = 400
        window_height = 400
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.configure(bg='light blue')

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="sys",
            auth_plugin="mysql_native_password"
        )
        self.cursor = self.mydb.cursor()

        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.p1 = tk.PhotoImage(file='Delete_icon.png')
        self.iconphoto(False, self.p1)

        self.frame = tk.Frame(self, bg='light blue')
        self.frame.pack(padx=20, pady=125)

        self.create_widgets()

    def create_widgets(self):
        self.heading_label = tk.Label(self.frame, text="Delete", font=("Georgia", 18, "bold"), bg='light blue')
        self.heading_label.grid(row=0, column=0, columnspan=5, pady=(10, 20), sticky="n")

        self.label1 = tk.Label(self.frame, text="ID", font=("Georgia", 10), bg='light blue')
        self.entry1 = tk.Entry(self.frame)

        self.back_button = tk.Button(self.frame, text="Back", command=self.go_back, font=("Georgia", 8))

        self.label1.grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.entry1.grid(row=1, column=1, padx=10, pady=5)

        self.img = tk.PhotoImage(file='delete_icon.png')
        self.delete_button = tk.Button(self.frame, image=self.img, compound='center', width=20, height=20, padx=5, pady=10, command=self.delete_meeting)
        self.delete_button.grid(row=1, column=2, columnspan=1, padx=10, pady=10, sticky="e")

        self.back_button.grid(row=2, column=0, padx=10, pady=10, sticky='sw')

    def delete_meeting(self):
        meeting_id = self.entry1.get()
        val = meeting_id.isdigit()
        id_check_query = "SELECT ID FROM events WHERE ID = %s"
        self.cursor.execute(id_check_query, (meeting_id,))
        existing_id = self.cursor.fetchone()
        if existing_id:
            result = messagebox.askokcancel("Confirmation", f"Are you sure you want to delete meeting ID {meeting_id}?")

            if result:
                delete_query = "DELETE FROM events WHERE ID=%s"
                self.cursor.execute(delete_query, (meeting_id,))
                self.mydb.commit()
                print("Meeting data deleted from the database")
            else:
                self.destroy()
                subprocess.run(["python", "delete.py"], shell=True)
        else:
            messagebox.showerror("Error", "Please enter a valid meeting ID.")

    def go_back(self):
        self.destroy()
        subprocess.run(["python", "adashboard.py"], shell=True)

if __name__ == "__main__":
    app = DeleteMeetingApp()
    app.mainloop()
