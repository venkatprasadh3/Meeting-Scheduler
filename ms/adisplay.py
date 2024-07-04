import tkinter as tk
from tkinter import ttk
from tkinter import Label, Scrollbar, Text
import mysql.connector
import subprocess

class DisplayWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Display")

        window_width = 450
        window_height = 610

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.configure(bg='light blue')

        self.frame = tk.Frame(self, bg='light blue')
        self.frame.pack(padx=20, pady=20,anchor='c')

        self.heading_label = tk.Label(self.frame, text="Display", font=("Georgia", 18, "bold"), bg='light blue')
        self.heading_label.grid(row=0, column=0, columnspan=5, pady=(10, 20), sticky="n")

        self.p1 = tk.PhotoImage(file='display.png')
        self.iconphoto(False, self.p1)
        
        self.create_text_widget()

        try:
            self.display_events()
        except mysql.connector.Error as error:
            self.event_text.insert("end", f"Error: {error}")

        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_back_button()

    def create_text_widget(self):
        self.event_text = Text(self.frame, wrap="none", width=40, height=20, font=("Georgia", 10), bg='light blue')
        self.event_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.scrollbar = Scrollbar(self.frame, command=self.event_text.yview)
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        self.event_text.config(yscrollcommand=self.scrollbar.set)

    def display_events(self):
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="sys",
            auth_plugin="mysql_native_password"
        )
        cursor = db_connection.cursor()

        select_query = "SELECT * FROM events"
        cursor.execute(select_query)
        events_data = cursor.fetchall()

        for event in events_data:
            event_details = (
                f"ID: {event[0]}\n"
                f"Title: {event[1]}\n"
                f"Date: {event[2]}\n"
                f"Time: {event[3]}\n"
                f"Link: {event[4]}\n"
                f"Location: {event[5]}\n"
                f"Description: {event[6]}\n\n"
            )
            self.event_text.insert("end", event_details)

        cursor.close()
        db_connection.close()

    def create_back_button(self):
        self.back_button = tk.Button(self.frame, text="Back", command=self.go_back, font=("Georgia", 8), bg='gray65')
        self.back_button.grid(row=3, column=0, padx=10, pady=10, sticky='sw')

    def go_back(self):
        self.destroy()
        subprocess.run(["python", "adashboard.py"], shell=True)

if __name__ == "__main__":
    app = DisplayWindow()
    app.mainloop()
