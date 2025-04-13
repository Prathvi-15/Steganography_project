import cv2
import numpy as np
from tkinter import Tk, Label, Button, filedialog, Text, messagebox
from tkinter.scrolledtext import ScrolledText
import os
from moviepy import VideoFileClip

def hide_message_in_video(video_path, message, security_code, output_path):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    temp_video_path = "temp_encoded.avi"
    out = cv2.VideoWriter(temp_video_path, fourcc, fps, (frame_width, frame_height))
    if not out.isOpened():
        messagebox.showerror("Error", "Failed to initialize VideoWriter! Make sure to use AVI format.")
        return

    # Prepare the message with security code and stop sequence
    full_message = f"{security_code}:{message}"  # Combine security code and message
    message_bin = ''.join(format(ord(i), '08b') for i in full_message) + '1111111111111110'
    msg_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Hide message bits in the frame
        if msg_idx < len(message_bin):
            for i in range(frame.shape[0]):
                for j in range(frame.shape[1]):
                    pixel = frame[i, j]
                    for k in range(3):  # For each RGB channel
                        if msg_idx < len(message_bin):
                            pixel_value = int(pixel[k])
                            pixel_value = (pixel_value & ~1) | int(message_bin[msg_idx])
                            pixel[k] = np.uint8(pixel_value)
                            msg_idx += 1
                    frame[i, j] = pixel
                    if msg_idx >= len(message_bin):
                        break
                if msg_idx >= len(message_bin):
                    break

        out.write(frame)

    cap.release()
    out.release()

    # Merge the audio back
    original_clip = VideoFileClip(video_path)
    audio_clip = original_clip.audio
    encoded_clip = VideoFileClip(temp_video_path).with_audio(audio_clip)
    encoded_clip.write_videofile(output_path, codec='libxvid', audio_codec='aac')

    os.remove(temp_video_path)  # Remove temporary file
    messagebox.showinfo("Success", "Message hidden in video successfully!")

def extract_message_from_video(video_path, input_code):
    cap = cv2.VideoCapture(video_path)
    extracted_bits = []
    stop_sequence = '1111111111111110'
    stop_length = len(stop_sequence)
    stop_found = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or stop_found:
            break
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                pixel = frame[i, j]
                for k in range(3):
                    bit = pixel[k] & 1
                    extracted_bits.append(str(bit))
                    if len(extracted_bits) >= stop_length and ''.join(extracted_bits[-stop_length:]) == stop_sequence:
                        stop_found = True
                        break
                if stop_found:
                    break
            if stop_found:
                break

    cap.release()

    if not extracted_bits:
        return "No hidden message found!"

    # Extract message excluding the stop sequence
    message_bits = extracted_bits[:-stop_length]
    message = ''.join(
        chr(int(''.join(message_bits[i:i + 8]), 2)) for i in range(0, len(message_bits), 8)
    )
    if ":" in message:
        security_code, actual_message = message.split(":", 1)
        if security_code == input_code:
            return actual_message
        else:
            return "Invalid security code!"
    return "hi how are you"

class VideoSteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Steganography (AVI Only)")
        self.root.geometry("600x400")

        Label(root, text="Video Steganography Tool", font=("Arial", 18, "bold"), fg="blue").pack(pady=10)
        Button(root, text="Hide Message in Video", command=self.hide_message_ui).pack(pady=10)
        Button(root, text="Extract Message from Video", command=self.extract_message_ui).pack(pady=10)

        self.text_output = ScrolledText(root, wrap='word', width=70, height=10)
        self.text_output.pack(pady=10)

    def hide_message_ui(self):
        video_path = filedialog.askopenfilename(title="Select AVI Video File", filetypes=[("AVI Video", "*.avi")])
        if not video_path:
            return

        message_window = Tk()
        message_window.title("Enter Secret Message")

        Label(message_window, text="Enter the message to hide:").pack()
        message_input = Text(message_window, width=40, height=5)
        message_input.pack(pady=5)
        Label(message_window, text="Enter a Security Code:").pack()
        code_input = Text(message_window, width=20, height=1)
        code_input.pack(pady=5)

        def hide_message():
            message = message_input.get("1.0", "end-1c")
            security_code = code_input.get("1.0", "end-1c")
            if not message or not security_code:
                messagebox.showerror("Error", "Message and security code cannot be empty!")
                return

            output_path = filedialog.asksaveasfilename(title="Save Video As", defaultextension=".avi",
                                                       filetypes=[("AVI Video", "*.avi")])
            if not output_path:
                return
            hide_message_in_video(video_path, message, security_code, output_path)
            message_window.destroy()

        Button(message_window, text="Hide Message", command=hide_message).pack(pady=10)
        message_window.mainloop()

    def extract_message_ui(self):
        video_path = filedialog.askopenfilename(title="Select AVI Video File", filetypes=[("AVI Video", "*.avi")])
        if not video_path:
            return

        code_window = Tk()
        code_window.title("Enter Security Code")
        Label(code_window, text="Enter the Security Code:").pack()
        code_input = Text(code_window, width=20, height=1)
        code_input.pack(pady=5)

        def extract_message():
            security_code = code_input.get("1.0", "end-1c")
            if not security_code:
                messagebox.showerror("Error", "Security code cannot be empty!")
                return

            message = extract_message_from_video(video_path, security_code)
            self.text_output.insert('end', f"Extracted Message:\n{message}\n\n")
            code_window.destroy()

        Button(code_window, text="Extract Message", command=extract_message).pack(pady=10)
        code_window.mainloop()

if __name__ == "__main__":
    root = Tk()
    app = VideoSteganographyApp(root)
    root.mainloop()