import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
import mysql.connector
import subprocess

class MeetingSchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Add")

        window_width = 400
        window_height = 550

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.configure(bg='light blue')

        p1 = tk.PhotoImage(file='add.png')
        self.iconphoto(False, p1)

        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.frame = tk.Frame(self, bg='light blue')
        self.frame.pack(padx=20, pady=20)

        self.setup_ui()

    def setup_ui(self):
        self.heading_label1 = tk.Label(self.frame, text="Add", font=("Georgia", 18, "bold"), bg='light blue')
        self.heading_label1.grid(row=0, column=0, columnspan=5, pady=(10, 20), sticky="n")

        self.row = 1
        self.meeting_id_label = tk.Label(self.frame, text="Meeting ID:", font=("Georgia", 10), bg='light blue')
        self.meeting_id_label.grid(row=self.row, column=0, sticky='w')
        self.meeting_id_entry = tk.Entry(self.frame)
        self.meeting_id_entry.grid(row=self.row, column=1, sticky='w', pady=10)

        self.row += 1
        self.title_label = tk.Label(self.frame, text="Title:", font=("Georgia", 10), bg='light blue')
        self.title_label.grid(row=self.row, column=0, sticky='w')
        self.title_entry = tk.Entry(self.frame)
        self.title_entry.grid(row=self.row, column=1, sticky='w', pady=10)

        self.row += 1
        self.date_label = tk.Label(self.frame, text="Date:", font=("Georgia", 10), bg='light blue')
        self.date_label.grid(row=self.row, column=0, sticky='w')
        self.cal = DateEntry(self.frame, selectmode='day')
        self.cal.grid(row=self.row, column=1, sticky='w', pady=10)

        self.time_values = []
        self.start_hour, self.start_minute = 8, 0
        self.end_hour, self.end_minute = 17, 0

        while self.start_hour < self.end_hour or (self.start_hour == self.end_hour and self.start_minute < self.end_minute):
            self.time_values.append(f"{self.start_hour:02d}:{self.start_minute:02d} AM" if self.start_hour < 12 else f"{self.start_hour-12:02d}:{self.start_minute:02d} PM")
            self.start_minute += 15
            if self.start_minute == 60:
                self.start_minute = 0
                self.start_hour += 1

        self.row += 1
        self.time_label = tk.Label(self.frame, text="Time:", font=("Georgia", 10), bg='light blue')
        self.time_label.grid(row=self.row, column=0, sticky='w')
        self.time_var = tk.StringVar()
        self.time_picker = ttk.Combobox(self.frame, textvariable=self.time_var, values=self.time_values)
        self.time_picker.grid(row=self.row, column=1, sticky='w', pady=10)

        self.row += 1
        self.link_label = tk.Label(self.frame, text="Meeting Link:", font=("Georgia", 10), bg='light blue')
        self.link_label.grid(row=self.row, column=0, sticky='w')
        self.link_entry = tk.Entry(self.frame)
        self.link_entry.grid(row=self.row, column=1, sticky='w', pady=10)

        self.row += 1
        self.location_label = tk.Label(self.frame, text="Location:", font=("Georgia", 10), bg='light blue')
        self.location_label.grid(row=self.row, column=0, sticky='nw')
        self.location_text = tk.Text(self.frame, height=3, width=30)
        self.location_text.grid(row=self.row, column=1, sticky='w', pady=10)

        self.row += 1
        self.description_label = tk.Label(self.frame, text="Description:", font=("Georgia", 10), bg='light blue')
        self.description_label.grid(row=self.row, column=0, sticky='nw')
        self.description_text = tk.Text(self.frame, height=5, width=30)
        self.description_text.grid(row=self.row, column=1, sticky='w', pady=10)

        self.row += 1
        self.submit_button = tk.Button(self.frame, text="Submit", font=("Georgia", 10), command=self.validate_input, bg='gray65')
        self.submit_button.grid(row=self.row, column=0, columnspan=2)

        self.row += 1
        self.back_button = tk.Button(self.frame, text="Back", font=("Georgia", 8), command=self.go_back, bg='gray65')
        self.back_button.grid(row=self.row, column=0, padx=10, pady=10, sticky='sw')

    def go_back(self):
        self.destroy()
        subprocess.run(["python", "adashboard.py"], shell=True)

    def validate_input(self):
        meeting_id = self.meeting_id_entry.get()
        title = self.title_entry.get()
        date_obj = self.cal.get_date()
        date = date_obj.strftime("%Y-%M-%D")
        time_str = self.time_var.get()
        time_obj = datetime.strptime(time_str, "%I:%M %p")
        time_formatted = time_obj.strftime("%H:%M:%S")
        link = self.link_entry.get()
        location = self.location_text.get("1.0", "end-1c")
        description = self.description_text.get("1.0", "end-1c")

        if not meeting_id.isdigit():
            messagebox.showerror("Invalid Input", "Meeting ID should be an integer.")
            return

        if not link.startswith("http://") and not link.startswith("https://"):
            messagebox.showerror("Invalid Input", "Meeting Link should start with 'http://' or 'https://'.")
            return
        
        confirm_message = f"Meeting ID: {meeting_id}\nTitle: {title}\nDate: {date}\nTime: {time_formatted}\nLink: {link}\nLocation: {location}\nDescription: {description}\n\nDo you want to submit this meeting?"

        result = messagebox.askyesno("Confirmation", confirm_message)

        if result:
            self.submit_meeting()

    def submit_meeting(self):
        meeting_id = self.meeting_id_entry.get()
        title = self.title_entry.get()
        date_obj = self.cal.get_date()
        date = date_obj.strftime("%Y-%m-%d")
        time_str = self.time_var.get()
        time_obj = datetime.strptime(time_str, "%I:%M %p")
        time_formatted = time_obj.strftime("%H:%M:%S")
        link = self.link_entry.get()
        location = self.location_text.get("1.0", "end-1c")
        description = self.description_text.get("1.0", "end-1c")

        try:
            mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="sys", auth_plugin="mysql_native_password")
            cursor = mydb.cursor()
            id_check_query = "SELECT ID FROM events WHERE ID = %s"
            cursor.execute(id_check_query, (meeting_id,))
            existing_id = cursor.fetchone()

            date_time_check_query = "SELECT ID FROM events WHERE Date = %s AND Time = %s"
            cursor.execute(date_time_check_query, (date, time_formatted))
            existing_date_time = cursor.fetchone()

            if existing_id:
                messagebox.showerror("Meeting ID Already Exists", "A meeting with the same Meeting ID already exists.")
            elif existing_date_time:
                messagebox.showerror("Meeting Date and Time Conflict", "A meeting with the same Date and Time already exists.")
            else:
                confirm_message = f"Meeting ID: {meeting_id}\nTitle: {title}\nDate: {date}\nTime: {time_formatted}\nLink: {link}\nLocation: {location}\nDescription: {description}\n\nDo you want to submit this meeting?"
                result = messagebox.askyesno("Confirmation", confirm_message)

                if result:
                    insert_query = "INSERT INTO events (ID, Title, Date, Time, Link, Location, Description) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    data = (meeting_id, title, date, time_formatted, link, location, description)
                    cursor.execute(insert_query, data)
                    mydb.commit()
                    print("Meeting data inserted into the database")

        except mysql.connector.Error as error:
            print("Error: {}".format(error))

        finally:
            cursor.close()
            mydb.close()
       
if __name__ == "__main__":
    app = MeetingSchedulerApp()
    app.mainloop()
