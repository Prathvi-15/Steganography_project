import onetimepad
from tkinter import *
from tkinter import messagebox


# Function to handle encoding
def encode_popup():
    def encryptMessage():
        pt = entry_message.get()  # Get plain text from the popup
        key = entry_key.get()  # Get key from the popup

        if not pt or not key:
            messagebox.showerror("Error", "Please provide both the message and the key.")
            return

        # Encrypt the message
        ct = onetimepad.encrypt(pt, key)

        # Display encrypted message with a copy option
        def copy_to_clipboard():
            root.clipboard_clear()
            root.clipboard_append(ct)
            root.update()  # Keep the clipboard updated
            messagebox.showinfo("Copied", "Encrypted message copied to clipboard!")

        popup.destroy()
        # Display result in a new popup
        result_popup = Toplevel(root)
        result_popup.title("Encrypted Message")
        result_popup.geometry("400x200")

        Label(result_popup, text="Encrypted Message:").pack(pady=10)
        message_label = Label(result_popup, text=ct, wraplength=350, bg="lightgray", width=40, height=2)
        message_label.pack(pady=10)

        Button(result_popup, text="Copy to Clipboard", command=copy_to_clipboard, bg="green", fg="white").pack(pady=10)

    # Create the encode popup
    popup = Toplevel(root)
    popup.title("Encode Message")
    popup.geometry("400x200")

    Label(popup, text="Enter Message:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    entry_message = Entry(popup, width=30)
    entry_message.grid(row=0, column=1, padx=10, pady=10)

    Label(popup, text="Enter Key:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    entry_key = Entry(popup, width=30)
    entry_key.grid(row=1, column=1, padx=10, pady=10)

    Button(popup, text="Encrypt", command=encryptMessage, bg="red", fg="white").grid(row=2, column=1, pady=20)


# Function to handle decoding
def decode_popup():
    def decryptMessage():
        ct = entry_cipher.get()  # Get cipher text from the popup
        key = entry_key.get()  # Get key from the popup

        if not ct or not key:
            messagebox.showerror("Error", "Please provide both the cipher text and the key.")
            return

        try:
            # Decrypt the message
            pt = onetimepad.decrypt(ct, key)
            messagebox.showinfo("Decrypted Message", f"Decrypted Text: {pt}")
            popup.destroy()
        except ValueError:
            messagebox.showerror("Error", "Decryption failed. Ensure the correct key is provided.")

    # Create the decode popup
    popup = Toplevel(root)
    popup.title("Decode Message")
    popup.geometry("400x200")

    Label(popup, text="Enter Cipher Text:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    entry_cipher = Entry(popup, width=30)
    entry_cipher.grid(row=0, column=1, padx=10, pady=10)

    Label(popup, text="Enter Key:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    entry_key = Entry(popup, width=30)
    entry_key.grid(row=1, column=1, padx=10, pady=10)

    Button(popup, text="Decrypt", command=decryptMessage, bg="green", fg="white").grid(row=2, column=1, pady=20)


# Main window setup
root = Tk()
root.title("CRYPTOGRAPHY")
root.geometry("300x200")

# Buttons for encoding and decoding
Button(root, text="Encode Message", command=encode_popup, bg="blue", fg="white", width=20).pack(pady=20)
Button(root, text="Decode Message", command=decode_popup, bg="orange", fg="white", width=20).pack(pady=20)

# Start the main loop
root.mainloop()