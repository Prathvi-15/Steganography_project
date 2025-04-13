from tkinter import *
import tkinter.filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Encryption:
    @staticmethod
    def generate_key(password):
        salt = b'salt_123'  # In production, use a random salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    @staticmethod
    def encrypt_message(message, key):
        f = Fernet(key)
        return f.encrypt(message.encode())

    @staticmethod
    def decrypt_message(encrypted_message, key):
        f = Fernet(key)
        return f.decrypt(encrypted_message).decode()


class ImageStegano:
    def __init__(self):
        self.image = None
        self.camera = None
        self.panel = None  # To store the image panel for live feed
        self.is_capturing = False

    def main(self, root):
        root.title("IMAGE STEGANOGRAPHY")
        root.geometry("500x700")
        root.resizable(width=False, height=False)
        root.config(bg="black")

        frame = Frame(root)
        frame.grid()

        title = Label(frame, text="IMAGE STEGANOGRAPHY", font=("Arial black", 25, "bold"), fg="white", bg="blue")
        title.grid(pady=10)

        load_button = Button(frame, text="LOAD IMAGE", command=lambda: self.load_image(frame),
                             padx=14, bg="red", fg="white")
        load_button.config(font=("Helvetica", 14))
        load_button.grid(pady=10)

        webcam_button = Button(frame, text="TAKE LIVE IMAGE", command=lambda: self.start_webcam(frame),
                               padx=14, bg="green", fg="white")
        webcam_button.config(font=("Helvetica", 14))
        webcam_button.grid(pady=10)

        encode_button = Button(frame, text="ENCODE MESSAGE", command=lambda: self.encode_frame(frame),
                               padx=14, bg="blue", fg="white")
        encode_button.config(font=("Helvetica", 14))
        encode_button.grid(pady=10)

        decode_button = Button(frame, text="DECODE MESSAGE", command=lambda: self.decode_frame(frame),
                               padx=14, bg="blue", fg="white")
        decode_button.config(font=("Helvetica", 14))
        decode_button.grid(pady=10)

    def load_image(self, frame):
        filepath = tkinter.filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
        )
        if not filepath:
            return

        self.image = Image.open(filepath)
        self.display_image(frame)

    def start_webcam(self, frame):
        """Start the webcam feed and allow the user to capture an image."""
        self.camera = cv2.VideoCapture(0)  # Use the first available camera
        self.is_capturing = True
        self.update_webcam_feed(frame)

        # Add the capture button once the webcam is started
        capture_button = Button(frame, text="CAPTURE IMAGE", command=lambda: self.capture_image(frame),
                                 padx=14, bg="blue", fg="white")
        capture_button.config(font=("Helvetica", 14))
        capture_button.grid(pady=10)

    def update_webcam_feed(self, frame):
        """Update the webcam feed in the GUI."""
        if self.is_capturing and self.camera.isOpened():
            ret, frame_data = self.camera.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame_data, cv2.COLOR_BGR2RGB)
                frame_image = Image.fromarray(frame_rgb)
                frame_image.thumbnail((400, 300))

                img = ImageTk.PhotoImage(frame_image)

                if self.panel is None:
                    self.panel = Label(frame, image=img)
                    self.panel.image = img
                    self.panel.grid(pady=10)
                else:
                    self.panel.configure(image=img)
                    self.panel.image = img

            # Update the feed every 20ms
            frame.after(20, self.update_webcam_feed, frame)

    def capture_image(self, frame):
        """Capture the current frame from the webcam and save it."""
        if self.camera.isOpened():
            ret, frame_data = self.camera.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame_data, cv2.COLOR_BGR2RGB)
                captured_image = Image.fromarray(frame_rgb)
                self.image = captured_image
                self.save_image()
                messagebox.showinfo("Info", "Image Captured and Saved Successfully!")
        else:
            messagebox.showerror("Error", "Webcam is not running.")

    def save_image(self):
        """Save the captured image to a file."""
        filepath = tkinter.filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        if filepath:
            self.image.save(filepath)

    def display_image(self, frame):
        img_thumb = self.image.resize((200, 200))
        img = ImageTk.PhotoImage(img_thumb)
        panel = Label(frame, image=img)
        panel.image = img
        panel.grid(pady=10)

    def encode_frame(self, frame):
        if not self.image:
            messagebox.showerror("Error", "Please load an image first!")
            return

        frame.destroy()
        encode_frame = Frame(root)
        encode_frame.grid()

        Label(encode_frame, text="ENTER THE MESSAGE", font=("Arial black", 25, "bold"), fg="white", bg="blue").grid(
            pady=15)
        text_box = Text(encode_frame, width=50, height=10)
        text_box.grid()

        Label(encode_frame, text="ENTER SECRET KEY", font=("Arial black", 15, "bold"), fg="white", bg="blue").grid(
            pady=5)
        key_entry = Entry(encode_frame, show="*")
        key_entry.grid()

        def encode_message():
            message = text_box.get("1.0", "end-1c")
            secret_key = key_entry.get()

            if not message or not secret_key:
                messagebox.showinfo("Alert", "Please enter both message and secret key.")
                return

            try:
                key = Encryption.generate_key(secret_key)
                encrypted_message = Encryption.encrypt_message(message, key)
                encrypted_message = base64.b64encode(encrypted_message).decode() + "###"

                message_bits = ''.join([format(ord(char), '08b') for char in encrypted_message])

                if len(message_bits) > self.image.width * self.image.height * 3:
                    messagebox.showerror("Error", "Message too long for this image!")
                    return

                pixels = self.image.load()
                bit_idx = 0
                for i in range(self.image.width):
                    for j in range(self.image.height):
                        r, g, b = pixels[i, j]
                        if bit_idx < len(message_bits):
                            r = (r & 254) | int(message_bits[bit_idx])  # Modify least significant bit
                            bit_idx += 1
                        if bit_idx < len(message_bits):
                            g = (g & 254) | int(message_bits[bit_idx])  # Modify least significant bit
                            bit_idx += 1
                        if bit_idx < len(message_bits):
                            b = (b & 254) | int(message_bits[bit_idx])  # Modify least significant bit
                            bit_idx += 1
                        pixels[i, j] = (r, g, b)

                output_filepath = tkinter.filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png")]
                )

                if output_filepath:
                    self.image.save(output_filepath)
                    messagebox.showinfo("Success", "Message encoded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Encoding failed: {str(e)}")

        encode_button = Button(encode_frame, text="ENCODE", command=encode_message,
                               font=("Arial black", 25, "bold"), fg="white", bg="blue")
        encode_button.grid(pady=15)

        cancel_button = Button(encode_frame, text="CANCEL", command=lambda: self.back(encode_frame),
                               font=("Arial black", 25, "bold"), fg="white", bg="blue")
        cancel_button.grid()

    def decode_frame(self, frame):
        if not self.image:
            messagebox.showerror("Error", "Please load an image first!")
            return

        frame.destroy()
        decode_frame = Frame(root)
        decode_frame.grid()

        Label(decode_frame, text="ENTER SECRET KEY", font=("Arial black", 15, "bold"), fg="white", bg="blue").grid(
            pady=15)
        key_entry = Entry(decode_frame, show="*")
        key_entry.grid()

        def decode_message():
            secret_key = key_entry.get()

            if not secret_key:
                messagebox.showinfo("Alert", "Please enter the secret key.")
                return

            try:
                key = Encryption.generate_key(secret_key)

                pixels = self.image.load()
                message_bits = ""

                for i in range(self.image.width):
                    for j in range(self.image.height):
                        r, g, b = pixels[i, j]
                        message_bits += str(r & 1)
                        message_bits += str(g & 1)
                        message_bits += str(b & 1)

                message = ""
                for i in range(0, len(message_bits), 8):
                    byte = message_bits[i:i + 8]
                    message += chr(int(byte, 2))

                encrypted_message = message.split("###")[0]
                encrypted_message = base64.b64decode(encrypted_message)

                decrypted_message = Encryption.decrypt_message(encrypted_message, key)

                messagebox.showinfo("Decoded Message", decrypted_message)

            except Exception as e:
                messagebox.showerror("Error", f"Decoding failed: {str(e)}")

        decode_button = Button(decode_frame, text="DECODE", command=decode_message,
                               font=("Arial black", 25, "bold"), fg="white", bg="blue")
        decode_button.grid(pady=15)

        cancel_button = Button(decode_frame, text="CANCEL", command=lambda: self.back(decode_frame),
                               font=("Arial black", 25, "bold"), fg="white", bg="blue")
        cancel_button.grid()

    def back(self, frame):
        """Go back to the main screen."""
        frame.destroy()
        self.main(root)


if __name__ == "__main__":
    root = Tk()
    app = ImageStegano()
    app.main(root)
    root.mainloop()
