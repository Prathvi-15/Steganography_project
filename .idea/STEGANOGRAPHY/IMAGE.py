import cv2
from tkinter import *
import tkinter.filedialog
import tkinter.simpledialog
from tkinter import messagebox
from PIL import ImageTk, Image
import numpy as np


class IMG_Stegno:
    def main(self, root):
        """Initialize the main window with Encode, Decode, and Capture options."""
        root.title('Image Steganography with Live Picture Tracking')
        root.geometry('500x650')
        root.resizable(width=False, height=False)
        root.config(bg='black')

        frame = Frame(root)
        frame.grid()

        # Title Label
        title = Label(frame, text='IMAGE STEGANOGRAPHY', font=('Arial black', 25, 'bold'), fg="white", bg="blue")
        title.grid(pady=10, row=0)

        # Encode Button
        encode_btn = Button(frame, text="ENCODE", command=lambda: self.encode_frame1(frame), padx=14, bg='blue', fg='white', font=('Helvetica', 14))
        encode_btn.grid(pady=10, row=1)

        # Decode Button
        decode_btn = Button(frame, text="DECODE", command=lambda: self.decode_frame1(frame), padx=14, bg='blue', fg='white', font=('Helvetica', 14))
        decode_btn.grid(pady=10, row=2)

        # Capture Button
        capture_btn = Button(frame, text="CAPTURE", command=self.capture_image, padx=14, bg='blue', fg='white', font=('Helvetica', 14))
        capture_btn.grid(pady=10, row=3)

    def back(self, frame):
        """Return to the main frame."""
        frame.destroy()
        self.main(root)

    def capture_image(self):
        """Capture an image from the webcam and save it."""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Unable to access the camera.")
            return

        messagebox.showinfo("Info", "Press 'C' to capture and 'Q' to quit.")
        while True:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "Failed to grab frame.")
                break

            cv2.imshow('Live Capture - Press "C" to capture', frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('c'):  # Capture
                file_path = tkinter.filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
                if file_path:
                    cv2.imwrite(file_path, frame)
                    messagebox.showinfo("Success", f"Image saved at {file_path}")
                break
            elif key == ord('q'):  # Quit without saving
                break

        cap.release()
        cv2.destroyAllWindows()

    def encode_frame1(self, frame):
        """Open the encoding frame to allow encoding a secret message into an image."""
        frame.destroy()
        encode_frame = Frame(root)
        encode_frame.grid()

        Label(encode_frame, text="SELECT IMAGE FILE", font=("Arial black", 15, "bold"), fg="white", bg="blue").grid(pady=10)
        select_image_btn = Button(encode_frame, text="SELECT IMAGE", command=lambda: self.select_image_encode(encode_frame), font=("Arial", 14), bg="blue", fg="white")
        select_image_btn.grid(pady=10)

        Button(encode_frame, text="CANCEL", command=lambda: self.back(encode_frame), font=("Arial", 14), bg="blue", fg="white").grid(pady=15)
        encode_frame.grid()

    def decode_frame1(self, frame):
        """Open the decoding frame to extract a secret message from an image."""
        frame.destroy()
        decode_frame = Frame(root)
        decode_frame.grid()

        Label(decode_frame, text="SELECT IMAGE FILE", font=("Arial black", 15, "bold"), fg="white", bg="blue").grid(pady=10)
        select_image_btn = Button(decode_frame, text="SELECT IMAGE", command=lambda: self.select_image_decode(decode_frame), font=("Arial", 14), bg="blue", fg="white")
        select_image_btn.grid(pady=10)

        Button(decode_frame, text="CANCEL", command=lambda: self.back(decode_frame), font=("Arial", 14), bg="blue", fg="white").grid(pady=15)
        decode_frame.grid()

    def select_image_encode(self, frame):
        """Allow the user to select an image file to encode the message into."""
        image_path = tkinter.filedialog.askopenfilename(filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
        if image_path:
            self.encode_message_into_image(frame, image_path)

    def select_image_decode(self, frame):
        """Allow the user to select an image file to decode the hidden message from."""
        image_path = tkinter.filedialog.askopenfilename(filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
        if image_path:
            self.decode_message_from_image(frame, image_path)

    def encode_message_into_image(self, frame, image_path):
        """Encode the secret message into the selected image."""
        secret_message = tkinter.simpledialog.askstring("Input", "Enter the secret message:")
        if not secret_message:
            messagebox.showinfo("Error", "No message entered.")
            return

        # Open the image
        img = cv2.imread(image_path)
        if img is None:
            messagebox.showerror("Error", "Failed to load image.")
            return

        # Add message length at the beginning of the message for decoding purposes
        message = str(len(secret_message)) + "|" + secret_message
        message_binary = ''.join(format(ord(c), '08b') for c in message)

        if len(message_binary) > img.size * 3:
            messagebox.showerror("Error", "Message too large to encode in this image.")
            return

        data_index = 0
        for row in img:
            for pixel in row:
                for i in range(3):  # Loop over the 3 color channels (BGR)
                    if data_index < len(message_binary):
                        pixel[i] = int(bin(pixel[i])[2:-1] + message_binary[data_index], 2)
                        data_index += 1

        output_image_path = tkinter.filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if output_image_path:
            cv2.imwrite(output_image_path, img)
            messagebox.showinfo("Success", f"Message encoded successfully in {output_image_path}")
        frame.destroy()
        self.main(root)

    def decode_message_from_image(self, frame, image_path):
        """Decode the hidden message from the selected image."""
        img = cv2.imread(image_path)
        if img is None:
            messagebox.showerror("Error", "Failed to load image.")
            return

        binary_message = ""
        for row in img:
            for pixel in row:
                for i in range(3):  # Loop over the 3 color channels (BGR)
                    binary_message += str(pixel[i] & 1)  # Extract the LSB (least significant bit)

        # Extract the first 16 bits for the length of the hidden message
        message_length_bin = binary_message[:16]
        if len(message_length_bin) < 16:
            messagebox.showerror("Error", "No hidden message length found.")
            return

        message_length = int(message_length_bin, 2)  # Convert the binary length to an integer
        binary_message = binary_message[16:]  # Remove the length portion from the binary message

        # Ensure we have enough bits to read the full message
        if len(binary_message) < message_length * 8:
            messagebox.showerror("Error", "Not enough data to decode the full message.")
            return

        # Extract the actual message bits
        decoded_message = ""
        for i in range(0, message_length * 8, 8):
            byte = binary_message[i:i + 8]
            decoded_message += chr(int(byte, 2))

        secret_message = decoded_message[:message_length]  # Extract only the specified length
        messagebox.showinfo("Decoded Message", f"Hidden message: {secret_message}")

        frame.destroy()
        self.main(root)

# Run the application
if __name__ == "__main__":
    root = Tk()
    app = IMG_Stegno()
    app.main(root)
    root.mainloop()
