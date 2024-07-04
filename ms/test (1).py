import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

def create_new_window():
    new_window = tk.Toplevel(root)
    new_window.title("New Window")


    # Add your widgets and content to the new window
    label = tk.Label(new_window, text="This is a new window")
    label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")

     # Load the original image and resize it to fit the new window
    original_image = Image.open("background.png")
    width, height = root.winfo_width(), root.winfo_height()
    resized_image = original_image.resize((width, height), ImageResampling.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)

    # Create a label with the resized background image
    background_label = tk.Label(root, image=photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = photo  # Keep a reference to avoid garbage collecti
    
    create_new_window_button = tk.Button(root, text="Create New Window", command=create_new_window)
    create_new_window_button.pack()

    root.mainloop()
