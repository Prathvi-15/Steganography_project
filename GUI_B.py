from tkinter import *
from tkinter import filedialog, simpledialog
import tkinter.messagebox
import subprocess
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# Initialize the main window
window = Tk()

# Set window title and properties
window.title("PYTHON STEGNOGRAPHY")
window.geometry("1166x718")
window.state('zoomed')
window.config(background="black")

# Load and resize the sign-in image
try:
    window.sign_in_image = Image.open('GUI PICS\\amma.jpg')
    window.sign_in_image = window.sign_in_image.resize((1679, 800))
    photo = ImageTk.PhotoImage(window.sign_in_image)

    # Display the resized image
    window.sign_in_image_label = Label(window, image=photo, bg='#FFFFFF')
    window.sign_in_image_label.image = photo
    window.sign_in_image_label.place(x=-10, y=0)
except Exception as e:
    print(f"Error loading background image: {e}")
    window.quit()

# Load other images
try:
    LOGOv = PhotoImage(file=os.path.join("GUI PICS", "GMAIL.png"))
    TXT = PhotoImage(file=os.path.join("GUI PICS", "TEXT.png"))
    IMG = PhotoImage(file=os.path.join("GUI PICS", "IMAGE.png"))
    AUD = PhotoImage(file=os.path.join("GUI PICS", "AUDIO.png"))
    VID = PhotoImage(file=os.path.join("GUI PICS", "VIDEO.png"))
    QUITv = PhotoImage(file=os.path.join("GUI PICS", "QUIT.png"))
except Exception as e:
    print(f"Error loading images: {e}")
    window.quit()

# Function to disable the close window event
def disable_event():
    pass

# Function to launch Text Steganography
def TXTS():
    tkinter.messagebox.showinfo("Welcome.", "You are about to use Text Steganography, press 'q' to quit.")
    cmd = 'python TEXT.py'
    subprocess.Popen(cmd, shell=True)

# Function to launch Image Steganography
def IMGS():
    tkinter.messagebox.showinfo("Welcome.", "You are about to use Image Steganography, press 'q' to quit.")
    cmd = 'python IMAGE.py'
    subprocess.Popen(cmd, shell=True)

# Function to launch Audio Steganography
def AUDS():
    tkinter.messagebox.showinfo("Welcome.", "You are about to use Audio Steganography, press 'q' to quit.")
    cmd = 'python AUDIO.py'
    subprocess.Popen(cmd, shell=True)

# Function to launch Video Steganography
def VIDS():
    tkinter.messagebox.showinfo("Welcome.", "You are about to use Video Steganography, press 'q' to quit.")
    cmd = 'python VIDEO.py'
    subprocess.Popen(cmd, shell=True)

# Permanent sender email and password (Hardcoded)
SENDER_EMAIL = "johnjohnwick135@gmail.com"
SENDER_PASSWORD = "bhdj udur auan wvxs"

# Function to send email via Gmail with file attachment
def send_email():
    try:
        # Disable the Send button to prevent multiple clicks
        send_gmail_button.config(state="disabled")

        # Prompt for recipient email and message content
        recipient_email = simpledialog.askstring("Recipient Email", "Enter the recipient's email address:")
        subject = simpledialog.askstring("Subject", "Enter the subject of the email:")
        message_body = simpledialog.askstring("Message", "Enter your message:")

        if not all([recipient_email, subject, message_body]):
            tkinter.messagebox.showerror("Error", "All fields are required.")
            send_gmail_button.config(state="normal")  # Re-enable the Send button
            return

        # Allow the user to select a file to attach
        file_path = filedialog.askopenfilename(title="Select a file to attach")

        # Create email message
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = recipient_email
        message["Subject"] = subject
        message.attach(MIMEText(message_body, "plain"))

        # Attach the file if selected
        if file_path:
            attachment = MIMEBase('application', 'octet-stream')
            with open(file_path, 'rb') as f:
                attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(file_path)}'
            )
            message.attach(attachment)

        # Connect to Gmail SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)

        tkinter.messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as e:
        tkinter.messagebox.showerror("Error", f"Failed to send email: {e}")
    finally:
        # Re-enable the Send button after the operation is finished
        send_gmail_button.config(state="normal")

# Buttons for each steganography option
bt1 = Button(window, compound="top", image=TXT, command=TXTS)
bt1.place(x=200, y=430)

bt1a = Button(window, compound="top", image=IMG, command=IMGS)
bt1a.place(x=500, y=430)

bt2 = Button(window, compound="top", image=AUD, command=AUDS)
bt2.place(x=800, y=430)

bt4 = Button(window, compound="top", image=VID, command=VIDS)
bt4.place(x=1100, y=430)

# Quit button
btQ = Button(window, compound="top", text="", image=QUITv, command=window.quit)
btQ.place(x=1450, y=20)

# Send via Gmail button
send_gmail_button = Button(window, text="Encoded message Send via Gmail", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=send_email)
send_gmail_button.place(x=620, y=670)

# Prevent window resizing and handle window close button
window.protocol("WM_DELETE_WINDOW", disable_event)

# Run the application
window.mainloop()
