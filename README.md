# 🕵️‍♂️ Multimedia Steganography Tool

## 📖 Description

The **Multimedia Steganography Tool** is a Python-based desktop application that allows users to securely hide and retrieve secret messages within various types of media: **images, audio files, PDFs, and real-time webcam captures**. The tool features a secure **OTP-based login system** to ensure user authentication and privacy.

Using intuitive GUI controls and multiple steganographic techniques, the tool enables real-time message encoding and decoding with a focus on both functionality and ease of use.

---

## ✨ Key Features

- 🔐 **OTP-Based Login System** – Secure and verified user authentication  
- 🖼️ **Image Steganography** – Hide/reveal messages in static images  
- 🎵 **Audio Steganography** – Encode/decode messages inside audio files  
- 📄 **PDF Steganography** – Embed and extract text from PDF documents  
- 📷 **Real-Time Webcam Capture** – Steganography using captured images  
- 🔒 **Encryption Support** – Optional message encryption before embedding  
- 🧑‍💻 **Graphical User Interface (GUI)** – User-friendly interface using Tkinter  

---

## 🛠️ Technologies Used

- **Python** – Core application logic  
- **Tkinter** – GUI development  
- **PIL (Pillow)** – Image processing  
- **PyPDF2 / fitz** – PDF manipulation  
- **pyaudio / wave / scipy** – Audio processing  
- **smtplib / random / email** – OTP verification  
- **OpenCV** – Real-time image capture (webcam)  
- **cryptography / base64** – Message encryption and encoding  

---

## ⚙️ Installation & Setup

### 🔧 Prerequisites

- Python 3.7 or higher installed  
- Internet connection for OTP (via email)  
- Webcam (for real-time image capture functionality)

### 📦 Install Required Libraries

Install all required Python packages using pip:

pip install pillow opencv-python numpy scipy pyaudio PyPDF2 python-docx cryptography

Run the Application
python main.py
