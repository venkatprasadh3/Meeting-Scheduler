import tkinter as tk
from tkinter import ttk
import mysql.connector
import subprocess

class SearchMeetingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Search Meeting")

        window_width = 400
        window_height = 500

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.configure(bg='light blue')

        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.frame = tk.Frame(self, bg='light blue')
        self.frame.pack(padx=20, pady=100)

        self.p1 = tk.PhotoImage(file='search_img.png')
        self.iconphoto(False, self.p1)

        self.create_widgets()

    def create_widgets(self):
        heading_label = tk.Label(self.frame, text="Search", font=("Georgia", 18, "bold"), bg='light blue')
        heading_label.grid(row=0, column=0, columnspan=5, pady=(10, 20), sticky="n")

        self.label1 = tk.Label(self.frame, text="Title", font=("Georgia", 10), bg='light blue')
        self.entry1 = tk.Entry(self.frame)

        self.event_text = tk.Text(self.frame, height=5, width=30)

        self.back_button = tk.Button(self.frame, text="Back", command=self.go_back, font=("Georgia", 8), bg='gray65')

        self.img = tk.PhotoImage(file='search_icon.png')
        self.search_button = tk.Button(self.frame, image=self.img, compound='center', width=20, height=20, padx=5, pady=10, command=self.search_meeting)

        self.label1.grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.entry1.grid(row=1, column=1, padx=10, pady=5)
        self.search_button.grid(row=1, column=2, columnspan=1, padx=20, pady=20, sticky="e")
        self.event_text.grid(row=2, column=0, columnspan=10, padx=20, pady=20, sticky="e")

        scrollbar = tk.Scrollbar(self.frame, command=self.event_text.yview)
        scrollbar.grid(row=2, column=10, sticky="e")
        self.event_text.config(yscrollcommand=scrollbar.set)
        self.back_button.grid(row=3, column=0, padx=10, pady=10, sticky='sw')

    def go_back(self):
        self.destroy()
        subprocess.run(["python", "adashboard.py"], shell=True)

    def search_meeting(self):
        title = self.entry1.get()
        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="sys",
                auth_plugin="mysql_native_password"
            )
            cursor = db_connection.cursor()

            select_query = "SELECT * FROM events WHERE Title LIKE '%" + title + "%' "
            cursor.execute(select_query)
            events_data = cursor.fetchall()

            if events_data:
                self.event_text.delete("1.0", "end")
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
            else:
                self.event_text.delete("1.0", "end")
                self.event_text.insert("end", "No events found with the specified title.")

            cursor.close()
            db_connection.close()
        except mysql.connector.Error as error:
            self.event_text.delete("1.0", "end")
            self.event_text.insert("end", f"Error: {error}")

if __name__ == "__main__":
    app = SearchMeetingApp()
    app.mainloop()
