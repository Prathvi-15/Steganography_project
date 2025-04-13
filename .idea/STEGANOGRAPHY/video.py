import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np


# Function to encode text into the video
def encode_text_to_video(video_path, text, output_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception(f"Error: Unable to open video file {video_path}")

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Add end marker to text and convert to binary
    text += '###'  # End marker
    binary_text = ''.join([format(ord(char), '08b') for char in text])
    binary_idx = 0

    print(f"Encoding the message with {len(binary_text)} bits of data...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Ensure the frame is writable
        frame = np.array(frame, dtype=np.uint8)

        # Modify the LSB of the blue channel to embed binary text
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                if binary_idx < len(binary_text):
                    pixel = list(frame[i, j])
                    pixel[0] = (pixel[0] & ~1) | int(binary_text[binary_idx])  # LSB modification
                    frame[i, j] = tuple(pixel)
                    binary_idx += 1

        out.write(frame)

    cap.release()
    out.release()

    print(f"Encoding finished. Output saved to {output_path}")
    return True


# Function to decode the hidden text from the video
def decode_text_from_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception(f"Error: Unable to open video file {video_path}")

    binary_text = ''
    print("Extracting binary data from video...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Traverse through the frame pixels to extract the LSBs
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                binary_text += str(frame[i, j][0] & 1)  # Extract LSB of the blue channel

    cap.release()

    # Debug: Print out the first 100 characters of binary string
    print("Decoded binary (first 100 characters):", binary_text[:100])

    # Split the binary text into 8-bit chunks (1 byte each)
    all_bytes = [binary_text[i:i + 8] for i in range(0, len(binary_text), 8)]
    decoded_text = ''

    # Decode the binary to ASCII characters
    for byte in all_bytes:
        try:
            char = chr(int(byte, 2))  # Convert binary to ASCII
            decoded_text += char
            # Check for the end marker
            if char == '#' and decoded_text[-2:] == '##':
                print("End marker detected. Decoding finished.")
                return decoded_text[:-2]  # Remove end marker and return message
        except ValueError:
            # Handle incomplete binary values gracefully
            break

    return "No hidden message found or message is corrupted!"


# GUI Function to open video file selection dialog
def select_video_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.avi *.mp4")])
    return file_path


# Function to handle encoding message into the video
def encode_message():
    video_path = select_video_file()
    if not video_path:
        return

    text = text_entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Error", "Please enter a message to encode.")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI Files", "*.avi")])
    if not save_path:
        return

    try:
        encode_text_to_video(video_path, text, save_path)
        messagebox.showinfo("Success", "Message encoded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to handle decoding message from the video
def decode_message():
    video_path = select_video_file()
    if not video_path:
        return

    try:
        message = decode_text_from_video(video_path)
        messagebox.showinfo("Decoded Message", f"Hidden message: {message}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Create GUI
root = tk.Tk()
root.title("Video Steganography")

frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

label = tk.Label(frame, text="Enter your message:")
label.grid(row=0, column=0, padx=5, pady=5)

text_entry = tk.Text(frame, width=40, height=5)
text_entry.grid(row=1, column=0, padx=5, pady=5)

encode_button = tk.Button(frame, text="Encode Message", command=encode_message)
encode_button.grid(row=2, column=0, pady=10)

decode_button = tk.Button(frame, text="Decode Message", command=decode_message)
decode_button.grid(row=3, column=0, pady=10)

# Run the GUI
try:
    root.mainloop()
except KeyboardInterrupt:
    print("Program interrupted. Exiting...")
