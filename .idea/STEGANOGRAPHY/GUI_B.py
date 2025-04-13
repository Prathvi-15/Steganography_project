from tkinter import *
import tkinter.messagebox
import subprocess
from PIL import Image, ImageTk

# Initialize the main window
window = Tk()

# Set window title and properties
# Set window title and properties
window.title("PYTHON STEGNOGRAPHY")
window.geometry("1166x718")
window.resizable(0, 0)
window.state('zoomed')
window.config(background="black")

window.sign_in_image = Image.open('LOGIN PICS\\background.png')
photo = ImageTk.PhotoImage(window.sign_in_image)
window.sign_in_image_label = Label(window, image=photo, bg='#FFFFFF')
window.sign_in_image_label.image = photo
window.sign_in_image_label.place(x=20, y=120)

# Load the images (make sure the images exist in the correct path)
try:
    LOGOv = PhotoImage(file="GUI PICS/LOGO.png")  # Replace with the correct path to your logo image
    TXT = PhotoImage(file="GUI PICS/TEXT.png")
    IMG = PhotoImage(file="GUI PICS/IMAGE.png")
    AUD = PhotoImage(file="GUI PICS/AUDIO.png")
    VID = PhotoImage(file="GUI PICS/VIDEO.png")
    QUITv = PhotoImage(file="GUI PICS/QUIT.png")
except Exception as e:
    print(f"Error loading images: {e}")
    window.quit()

# Function to disable the close window event
def disable_event():
    pass

# Function to launch Text Steganography
def TXTS():
    tkinter.messagebox.showinfo("Welcome.", "You are about to use Text Steganography, press 'q' to quit.")
    cmd = 'python TEXT.py'  # Ensure TEXT.py is in the same directory or provide the full path
    p = subprocess.Popen(cmd, shell=True)

# Function to launch Image Steganography
def IMGS():
    tkinter.messagebox.showinfo("Welcome.", "You are about to use Image Steganography, press 'q' to quit.")
    cmd = 'python IMAGE.py'  # Ensure IMAGE.py is in the same directory or provide the full path
    p = subprocess.Popen(cmd, shell=True)

# Function to launch Audio Steganography
def AUDS():
    tkinter.messagebox.showinfo("Welcome.", "You are about to use Audio Steganography, press 'q' to quit.")
    cmd = 'python AUDIO.py'  # Ensure AUDIO.py is in the same directory or provide the full path
    p = subprocess.Popen(cmd, shell=True)

# Function to launch Video Steganography
def VIDS():
    tkinter.messagebox.showinfo("Welcome.", "You are about to use Video Steganography, press 'q' to quit.")
    cmd = 'python VIDEO.py'  # Ensure VIDEO.py is in the same directory or provide the full path
    p = subprocess.Popen(cmd, shell=True)

# Logo image on the window


# Instructional label
lbl = Label(window, text="CHOOSE YOUR SELECTION FROM BELOW OPTIONS", font=('Arial black', 30))
lbl.place(x=200, y=200)

# Buttons for each steganography option
bt1 = Button(window, compound="top", text="TEXT STEGANOGRAPHY", image=TXT, command=TXTS)
bt1.place(x=200, y=350)

bt1a = Button(window, compound="top", text="IMAGE STEGANOGRAPHY", image=IMG, command=IMGS)
bt1a.place(x=500, y=350)

bt2 = Button(window, compound="top", text="AUDIO STEGANOGRAPHY", image=AUD, command=AUDS)
bt2.place(x=800, y=350)

bt4 = Button(window, compound="top", text="VIDEO STEGANOGRAPHY", image=VID, command=VIDS)
bt4.place(x=1100, y=350)

# Quit button
btQ = Button(window, compound="top", text="QUIT", image=QUITv, command=window.quit)
btQ.place(x=1200, y=20)

# Prevent window resizing and handle window close button
window.protocol("WM_DELETE_WINDOW", disable_event)

# Run the application
window.mainloop()
