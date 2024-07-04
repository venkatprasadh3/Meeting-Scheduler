import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk
import mysql.connector
from tkinter import PhotoImage
from datetime import datetime
import subprocess

class ModifyMeetingApp:
    def __init__(self, root):
        self.window = root
        self.window.title("Modify")

        window_width = 400
        window_height = 550

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.window.configure(bg='light blue')
        p1 = PhotoImage(file='modify.png')
        self.window.iconphoto(False, p1)
        style = ttk.Style(self.window)
        style.theme_use('clam')
        
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.window, bg='light blue')
        frame.pack(padx=20, pady=20)
        self.heading_label1 = tk.Label(frame, text="Modify", font=("Georgia", 18, "bold"), bg='light blue')
        self.heading_label1.grid(row=0, column=0, columnspan=5, pady=(10, 20), sticky="n")

        self.row = 1
        self.meeting_id_label = tk.Label(frame, text="Meeting ID:", font=("Georgia", 10), bg='light blue')
        self.meeting_id_label.grid(row=self.row, column=0, sticky='w')
        self.meeting_id_entry = tk.Entry(frame)
        self.meeting_id_entry.grid(row=self.row, column=1, sticky='w', pady=10)

        self.row += 1
        self.title_label = tk.Label(frame, text="Title:", font=("Georgia", 10), bg='light blue')
        self.title_label.grid(row=self.row, column=0, sticky='w')
        self.title_entry = tk.Entry(frame)
        self.title_entry.grid(row=self.row, column=1, sticky='w', pady=10)

        self.row += 1
        self.date_label = tk.Label(frame, text="Date:", font=("Georgia", 10), bg='light blue')
        self.date_label.grid(row=self.row, column=0, sticky='w')
        self.cal = DateEntry(frame, selectmode='day')
        self.cal.grid(row=self.row, column=1, sticky='w', pady=10)

        self.time_values = []
        self.start_hour, self.start_minute = 8, 0
        self.end_hour, self.end_minute = 17, 0

        while self.start_hour < self.end_hour or (self.start_hour == self.end_hour and self.start_minute < self.end_minute):
            time_str = (
                f"{self.start_hour:02d}:{self.start_minute:02d} AM"
                if self.start_hour < 12
                else f"{self.start_hour - 12:02d}:{self.start_minute:02d} PM"
            )
            self.time_values.append(time_str)
            self.start_minute += 15
            if self.start_minute == 60:
                self.start_minute = 0
                self.start_hour += 1

        self.row += 1
        self.time_label = tk.Label(frame, text="Time:", font=("Georgia", 10), bg='light blue')
        self.time_label.grid(row=self.row, column=0, sticky='w')
        self.time_var = tk.StringVar()
        self.time_picker = ttk.Combobox(frame, textvariable=self.time_var, values=self.time_values)
        self.time_picker.grid(row=self.row, column=1, sticky='w', pady=10)

        self.row += 1
        self.link_label = tk.Label(frame, text="Meeting Link:", font=("Georgia", 10), bg='light blue')
        self.link_label.grid(row=self.row, column=0, sticky='w')
        self.link_entry = tk.Entry(frame)
        self.link_entry.grid(row=self.row, column=1, sticky='w', pady=10)

        self.row += 1
        self.location_label = tk.Label(frame, text="Location:", font=("Georgia", 10), bg='light blue')
        self.location_label.grid(row=self.row, column=0, sticky='nw')
        self.location_text = tk.Text(frame, height=3, width=30)
        self.location_text.grid(row=self.row, column=1, sticky='w', pady=10)

        self.row += 1
        self.description_label = tk.Label(frame, text="Description:", font=("Georgia", 10), bg='light blue')
        self.description_label.grid(row=self.row, column=0, sticky='nw')
        self.description_text = tk.Text(frame, height=5, width=30)
        self.description_text.grid(row=self.row, column=1, sticky='w', pady=10)

        self.row += 1
        self.submit_button = tk.Button(frame, text="Submit", font=("Georgia", 10), command=self.validate_input, bg='gray65')
        self.submit_button.grid(row=self.row, column=0, columnspan=2)

        self.row += 1
        self.back_button = tk.Button(frame, text="Back", font=("Georgia", 8), command=self.go_back, bg='gray65')
        self.back_button.grid(row=self.row, column=0, padx=10, pady=10, sticky='sw')

    def go_back(self):
        self.window.destroy()
        subprocess.run(["python", "adashboard.py"], shell=True)

    def validate_input(self):
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
        else:
            self.window.destroy()
            subprocess.run(["python", "modify.py"], shell=True)

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
            date_time_check_query = "SELECT ID FROM events WHERE Date = %s AND Time = %s"
            cursor.execute(date_time_check_query, (date, time_formatted))
            existing_date_time = cursor.fetchone()

            if existing_date_time:
                messagebox.showerror("Meeting Date and Time Conflict", "A meeting with the same Date and Time already exists.")
            else:
                confirm_message = f"Meeting ID: {meeting_id}\nTitle: {title}\nDate: {date}\nTime: {time_formatted}\nLink: {link}\nLocation: {location}\nDescription: {description}\n\nDo you want to submit this meeting?"
                result = messagebox.askyesno("Confirmation", confirm_message)

                if result:
                    delete_query = "DELETE FROM events WHERE ID=%s"
                    cursor.execute(delete_query, (meeting_id,))
                    mydb.commit()
                    insert_query = "INSERT INTO events (ID, Title, Date, Time, Link, Location, Description) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    data = (meeting_id, title, date, time_formatted, link, location, description)
                    cursor.execute(insert_query, data)
                    mydb.commit()
                    print("Modified meeting data inserted into the database")

        except mysql.connector.Error as error:
            print("Error: {}".format(error))
        finally:
            cursor.close()
            mydb.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModifyMeetingApp(root)
    root.mainloop()
