import tkinter.filedialog
from tkinter import *

import tkinter.filedialog
from tkinter import messagebox
import wave
import numpy as np
from io import BytesIO
import pyaudio
import threading
import time
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class AudioRecorder:
    def __init__(self):
        self.recording = False
        self.frames = []
        self.audio = pyaudio.PyAudio()

    def start_recording(self):
        self.recording = True
        self.frames = []
        threading.Thread(target=self._record).start()

    def stop_recording(self):
        self.recording = False

    def _record(self):
        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=2,
            rate=44100,
            input=True,
            frames_per_buffer=1024
        )

        while self.recording:
            data = stream.read(1024)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()

    def save_recording(self, filename):
        if not self.frames:
            return False

        wf = wave.open(filename, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        return True


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


class AudioStegano:
    def __init__(self):
        self.recorder = AudioRecorder()

    def main(self, root):
        root.title("AUDIO STEGANOGRAPHY")
        root.geometry("500x700")
        root.resizable(width=False, height=False)
        root.config(bg="black")

        frame = Frame(root)
        frame.grid()

        title = Label(frame, text="AUDIO STEGANOGRAPHY", font=("Arial black", 25, "bold"), fg="white", bg="blue")
        title.grid(pady=10)

        record_button = Button(frame, text="RECORD AUDIO", command=lambda: self.record_frame(frame),
                               padx=14, bg="red", fg="white")
        record_button.config(font=("Helvetica", 14))
        record_button.grid(pady=10)

        encode_button = Button(frame, text="ENCODE", command=lambda: self.encode_frame(frame),
                               padx=14, bg="blue", fg="white")
        encode_button.config(font=("Helvetica", 14))
        encode_button.grid(pady=10)

        decode_button = Button(frame, text="DECODE", command=lambda: self.decode_frame(frame),
                               padx=14, bg="blue", fg="white")
        decode_button.config(font=("Helvetica", 14))
        decode_button.grid(pady=10)

    def record_frame(self, frame):
        frame.destroy()
        record_frame = Frame(root)
        record_frame.grid()

        status_label = Label(record_frame, text="Press Start to begin recording",
                             font=("Arial", 12), fg="white", bg="blue")
        status_label.grid(pady=10)

        def start_recording():
            self.recorder.start_recording()
            status_label.config(text="Recording...")
            start_button.config(state=DISABLED)
            stop_button.config(state=NORMAL)

        def stop_recording():
            self.recorder.stop_recording()
            filepath = tkinter.filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV files", "*.wav")]
            )
            if filepath:
                if self.recorder.save_recording(filepath):
                    messagebox.showinfo("Success", "Recording saved successfully!")
                else:
                    messagebox.showerror("Error", "Failed to save recording!")
            self.back(record_frame)

        start_button = Button(record_frame, text="START RECORDING",
                              command=start_recording, bg="green", fg="white")
        start_button.grid(pady=10)

        stop_button = Button(record_frame, text="STOP RECORDING",
                             command=stop_recording, bg="red", fg="white", state=DISABLED)
        stop_button.grid(pady=10)

        cancel_button = Button(record_frame, text="CANCEL",
                               command=lambda: self.back(record_frame), bg="gray", fg="white")
        cancel_button.grid(pady=10)

    def encode_frame(self, frame):
        filepath = tkinter.filedialog.askopenfilename(
            filetypes=[("WAV files", "*.wav")]
        )
        if not filepath:
            return
        self.encode_text_into_audio(frame, filepath)

    def encode_text_into_audio(self, frame, filepath):
        frame.destroy()
        encode_frame = Frame(root)
        encode_frame.grid()

        # Load audio file
        try:
            audio = wave.open(filepath, mode="rb")
            frames = bytearray(list(audio.readframes(audio.getnframes())))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open audio file: {str(e)}")
            return

        Label(encode_frame, text="ENTER THE MESSAGE",
              font=("Arial black", 25, "bold"), fg="white", bg="blue").grid(pady=15)
        text_box = Text(encode_frame, width=50, height=10)
        text_box.grid()

        Label(encode_frame, text="ENTER SECRET KEY",
              font=("Arial black", 15, "bold"), fg="white", bg="blue").grid(pady=5)
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

                if len(message_bits) > len(frames):
                    messagebox.showerror("Error", "Message too long for this audio file!")
                    return

                for i in range(len(message_bits)):
                    frames[i] = (frames[i] & 254) | int(message_bits[i])

                output_filepath = tkinter.filedialog.asksaveasfilename(
                    defaultextension=".wav",
                    filetypes=[("WAV files", "*.wav")]
                )

                if not output_filepath:
                    return

                with wave.open(output_filepath, "wb") as new_audio:
                    new_audio.setparams(audio.getparams())
                    new_audio.writeframes(frames)

                messagebox.showinfo("Success", "Message encoded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Encoding failed: {str(e)}")
            finally:
                audio.close()

        encode_button = Button(encode_frame, text="ENCODE", command=encode_message,
                               font=("Arial black", 25, "bold"), fg="white", bg="blue")
        encode_button.grid(pady=15)

        cancel_button = Button(encode_frame, text="CANCEL",
                               command=lambda: self.back(encode_frame),
                               font=("Arial black", 25, "bold"), fg="white", bg="blue")
        cancel_button.grid()

    def decode_frame(self, frame):
        filepath = tkinter.filedialog.askopenfilename(
            filetypes=[("WAV files", "*.wav")]
        )
        if not filepath:
            return
        self.decode_text_from_audio(frame, filepath)

    def decode_text_from_audio(self, frame, filepath):
        frame.destroy()
        decode_frame = Frame(root)
        decode_frame.grid()

        Label(decode_frame, text="ENTER SECRET KEY",
              font=("Arial black", 15, "bold"), fg="white", bg="blue").grid(pady=5)
        key_entry = Entry(decode_frame, show="*")
        key_entry.grid()

        def decode_message():
            secret_key = key_entry.get()
            if not secret_key:
                messagebox.showinfo("Alert", "Please enter the secret key.")
                return

            try:
                audio = wave.open(filepath, mode="rb")
                frames = bytearray(list(audio.readframes(audio.getnframes())))

                message_bits = []
                for byte in frames:
                    message_bits.append(str(byte & 1))

                binary_message = "".join(message_bits)
                chars = []
                for i in range(0, len(binary_message), 8):
                    byte = binary_message[i:i + 8]
                    if len(byte) == 8:
                        chars.append(chr(int(byte, 2)))

                encrypted_message = "".join(chars).split("###")[0]

                key = Encryption.generate_key(secret_key)
                encrypted_bytes = base64.b64decode(encrypted_message.encode())
                decrypted_message = Encryption.decrypt_message(encrypted_bytes, key)

                text_box = Text(decode_frame, width=50, height=10)
                text_box.insert(INSERT, decrypted_message)
                text_box.configure(state="disabled")
                text_box.grid(pady=10)
            except Exception as e:
                messagebox.showerror("Error", f"Decoding failed: {str(e)}")
            finally:
                audio.close()

        decode_button = Button(decode_frame, text="DECODE", command=decode_message,
                               font=("Arial black", 25, "bold"), fg="white", bg="blue")
        decode_button.grid(pady=15)

        cancel_button = Button(decode_frame, text="CANCEL",
                               command=lambda: self.back(decode_frame),
                               font=("Arial black", 25, "bold"), fg="white", bg="blue")
        cancel_button.grid()

    def back(self, frame):
        frame.destroy()
        self.main(root)


root = Tk()
app = AudioStegano()
app.main(root)
root.mainloop()

from tkinter import messagebox
import wave
import numpy as np
from io import BytesIO
import pyaudio
import threading
import time
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class AudioRecorder:
    def __init__(self):
        self.recording = False
        self.frames = []
        self.audio = pyaudio.PyAudio()

    def start_recording(self):
        if self.recording:
            return
        self.recording = True
        self.frames = []
        threading.Thread(target=self._record).start()

    def stop_recording(self):
        if not self.recording:
            return
        self.recording = False

    def _record(self):
        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=2,
            rate=44100,
            input=True,
            frames_per_buffer=1024
        )

        while self.recording:
            try:
                data = stream.read(1024)
                self.frames.append(data)
            except Exception as e:
                print(f"Recording error: {e}")
                break

        stream.stop_stream()
        stream.close()

    def save_recording(self, filename):
        if not self.frames:
            return False

        wf = wave.open(filename, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        return True


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


class AudioStegano:
    def __init__(self):
        self.recorder = AudioRecorder()

    def main(self, root):
        root.title("AUDIO STEGANOGRAPHY")
        root.geometry("500x700")
        root.resizable(width=False, height=False)
        root.config(bg="black")

        frame = Frame(root)
        frame.grid()

        title = Label(frame, text="AUDIO STEGANOGRAPHY", font=("Arial black", 25, "bold"), fg="white", bg="blue")
        title.grid(pady=10)

        record_button = Button(frame, text="RECORD AUDIO", command=lambda: self.record_frame(frame),
                               padx=14, bg="red", fg="white")
        record_button.config(font=("Helvetica", 14))
        record_button.grid(pady=10)

        encode_button = Button(frame, text="ENCODE", command=lambda: self.encode_frame(frame),
                               padx=14, bg="blue", fg="white")
        encode_button.config(font=("Helvetica", 14))
        encode_button.grid(pady=10)

        decode_button = Button(frame, text="DECODE", command=lambda: self.decode_frame(frame),
                               padx=14, bg="blue", fg="white")
        decode_button.config(font=("Helvetica", 14))
        decode_button.grid(pady=10)

    def record_frame(self, frame):
        frame.destroy()
        record_frame = Frame(root)
        record_frame.grid()

        status_label = Label(record_frame, text="Press Start to begin recording",
                             font=("Arial", 12), fg="white", bg="blue")
        status_label.grid(pady=10)

        def start_recording():
            self.recorder.start_recording()
            status_label.config(text="Recording...")
            start_button.config(state=DISABLED)
            stop_button.config(state=NORMAL)

        def stop_recording():
            self.recorder.stop_recording()
            filepath = tkinter.filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV files", "*.wav")]
            )
            if filepath:
                if self.recorder.save_recording(filepath):
                    messagebox.showinfo("Success", "Recording saved successfully!")
                else:
                    messagebox.showerror("Error", "Failed to save recording!")
            self.back(record_frame)

        start_button = Button(record_frame, text="START RECORDING",
                              command=start_recording, bg="green", fg="white")
        start_button.grid(pady=10)

        stop_button = Button(record_frame, text="STOP RECORDING",
                             command=stop_recording, bg="red", fg="white", state=DISABLED)
        stop_button.grid(pady=10)

        cancel_button = Button(record_frame, text="CANCEL",
                               command=lambda: self.back(record_frame), bg="gray", fg="white")
        cancel_button.grid(pady=10)

    def back(self, frame):
        frame.destroy()
        self.main(root)


if __name__ == "__main__":
    root = Tk()
    app = AudioStegano()
    app.main(root)
    root.mainloop()
