import os
from tkinter import *
import subprocess
import tkinter.messagebox
from PIL import ImageTk, Image

# Hardcoded Admin Credentials
ADMIN_EMAIL = "prathvikadoor@gmail.com"  # Replace with actual admin email
ADMIN_PASSWORD = "Prath@200415"  # Replace with actual admin password


def login():
    email = email_login.get().strip()
    password = password_login.get().strip()

    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        tkinter.messagebox.showinfo("Login", "Login successful")
        subprocess.run(["python", "otp.py"])  # Run the next file after successful login
    else:
        tkinter.messagebox.showerror("Error", "Invalid email or password.")


# Initialize GUI
gui = Tk()
gui.geometry("1166x718")
gui.resizable(0, 0)
gui.state('zoomed')
gui.config(background='#87CEEB')

# Add Background Image
bg_image_path = os.path.join('LOGIN PICS', 'background2.jpg')
image = Image.open(bg_image_path)
resized_image = image.resize((1600, 900))  # Resize to fit the window (width=800, height=600)
bg_image = ImageTk.PhotoImage(resized_image)

# Display the resized image
Label(gui, image=bg_image, bg='#FFFFFF').place(x=-3, y=-40)

# Login Frame
lgn_frame = Frame(gui, bg='white', width=360, height=400)
lgn_frame.place(x=600, y=150)

# Icons
username_icon_path = os.path.join('LOGIN PICS', 'username_icon.jpg')
username_icon = ImageTk.PhotoImage(Image.open(username_icon_path))
Label(lgn_frame, image=username_icon, bg='white').place(x=20, y=180)

gui.username_icon = Image.open('LOGIN PICS\\png.jpg')
photo = ImageTk.PhotoImage(gui.username_icon)
gui.username_icon_label = Label(gui, image=photo, bg='white')
gui.username_icon_label.image = photo
gui.username_icon_label.place(x=730, y=190)


password_icon_path = os.path.join('LOGIN PICS', 'password_icon.jpg')
password_icon = ImageTk.PhotoImage(Image.open(password_icon_path))
Label(lgn_frame, image=password_icon, bg='white').place(x=20, y=257)

# Buttons
Button(gui, text="BACK", font=("yu gothic ui", 13, "bold"), width=5, bd=0, bg='#3047ff', cursor='hand2',
       command=gui.quit, activebackground='#3047ff', fg='white').place(x=607, y=160)
Button(gui, text="LOGIN", font=("yu gothic ui", 13, "bold"), width=25, bd=0, bg='#3047ff',
       cursor='hand2', command=login, activebackground='#3047ff', fg='white').place(x=660, y=450)

# Labels and Entries
Label(gui, text="EMAIL ID", bg="white", fg="black", font=("yu gothic ui", 13, "bold")).place(x=737, y=300)
Label(gui, text="PASSWORD", bg="white", fg="black", font=("yu gothic ui", 13, "bold")).place(x=730, y=380)
email_login = Entry(gui)
password_login = Entry(gui, show="*")
email_login.place(x=660, y=335, width=270)
password_login.place(x=660, y=410, width=270)

gui.mainloop()
