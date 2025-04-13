import cv2
import numpy as np
from tkinter import Tk, Label, Button, filedialog, Text, messagebox
from tkinter.scrolledtext import ScrolledText
import os


def get_video_codec(file_path):
    """Detect video codec of the input video."""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == '.mp4':
        return 'mp4v'  # Codec for MP4
    elif ext == '.avi':
        return 'XVID'  # Codec for AVI
    else:
        return 'XVID'  # Default to XVID


def hide_message_in_video(video_path, message, output_path):
    cap = cv2.VideoCapture(video_path)

    # Dynamically detect codec and video properties
    codec = get_video_codec(video_path)
    fourcc = cv2.VideoWriter_fourcc(*codec)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    message_bin = ''.join(format(ord(i), '08b') for i in message) + '1111111111111110'  # Stop sequence
    msg_idx = 0
    print(f"Encoded message in binary: {message_bin}")  # Debug print for the binary message

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Embed message bits into LSB of pixel values
        if msg_idx < len(message_bin):
            for i in range(frame.shape[0]):
                for j in range(frame.shape[1]):
                    pixel = frame[i, j]
                    for k in range(3):  # R, G, B channels
                        if msg_idx < len(message_bin):
                            pixel_value = int(pixel[k])  # Ensure pixel value is int
                            pixel_value = (pixel_value & ~1) | int(message_bin[msg_idx])  # Replace LSB
                            pixel[k] = np.uint8(pixel_value)  # Ensure uint8 type
                            msg_idx += 1
                    frame[i, j] = pixel
                    if msg_idx >= len(message_bin):
                        break
                if msg_idx >= len(message_bin):
                    break
        out.write(frame)

    cap.release()
    out.release()
    messagebox.showinfo("Success", "Message hidden in video successfully!")


def extract_message_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    extracted_bits = []
    stop_sequence = '1111111111111110'
    stop_length = len(stop_sequence)
    stop_found = False

    print("Extracting message...")  # Debug print for message extraction process

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or stop_found:
            break

        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                pixel = frame[i, j]
                for k in range(3):  # R, G, B channels
                    bit = int(pixel[k]) & 1  # Extract LSB
                    extracted_bits.append(str(bit))

                    # Debugging: Print the extracted bits (comment out later)
                    if len(extracted_bits) % 1000 == 0:  # Print every 1000 bits
                        print(f"Extracted bits so far: {''.join(extracted_bits[-100:])}")

                    # Check for stop sequence
                    if len(extracted_bits) >= stop_length and ''.join(extracted_bits[-stop_length:]) == stop_sequence:
                        stop_found = True
                        break
                if stop_found:
                    break
            if stop_found:
                break

    cap.release()

    if not extracted_bits:
        return "ashish"

    # Extract message excluding the stop sequence
    message_bits = extracted_bits[:-stop_length]

    try:
        message = ''.join(
            chr(int(''.join(message_bits[i:i + 8]), 2)) for i in range(0, len(message_bits), 8)
        )
    except ValueError:
        message = "Error: Could not decode message. Binary data might be corrupted."

    print(f"Extracted message: {message}")  # Debug print for the decoded message

    return message


class VideoSteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Steganography")
        self.root.geometry("600x400")

        Label(root, text="Video Steganography Tool", font=("Arial", 18, "bold"), fg="blue").pack(pady=10)

        Button(root, text="Hide Message in Video", command=self.hide_message_ui).pack(pady=10)
        Button(root, text="Extract Message from Video", command=self.extract_message_ui).pack(pady=10)

        self.text_output = ScrolledText(root, wrap='word', width=70, height=10)
        self.text_output.pack(pady=10)

    def hide_message_ui(self):
        video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4 *.avi")])
        if not video_path:
            return

        message_window = Tk()
        message_window.title("Enter Secret Message")

        Label(message_window, text="Enter the message to hide:").pack()
        message_input = Text(message_window, width=40, height=5)
        message_input.pack(pady=10)

        def hide_message():
            message = message_input.get("1.0", "end-1c")
            if not message:
                messagebox.showerror("Error", "Message cannot be empty!")
                return
            output_ext = os.path.splitext(video_path)[1]  # Get same extension
            output_path = filedialog.asksaveasfilename(title="Save Video As", defaultextension=output_ext,
                                                       filetypes=[("Video Files", f"*{output_ext}")])
            if not output_path:
                return
            hide_message_in_video(video_path, message, output_path)
            message_window.destroy()

        Button(message_window, text="Hide Message", command=hide_message).pack(pady=10)
        message_window.mainloop()

    def extract_message_ui(self):
        video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4 *.avi")])
        if not video_path:
            return
        message = extract_message_from_video(video_path)
        self.text_output.insert('end', f"Extracted Message:\n{message}\n\n")


if __name__ == "__main__":
    root = Tk()
    app = VideoSteganographyApp(root)
    root.mainloop()
