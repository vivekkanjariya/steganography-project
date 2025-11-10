import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import stepic
import hashlib
from datetime import datetime
import os


# blockchain code
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data        # Image hash stored here
        self.previous_hash = previous_hash
        self.hash = self.calc_hash()

    def calc_hash(self):
        data_string = str(self.index) + self.timestamp + self.data + self.previous_hash
        return hashlib.sha256(data_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis()

    def create_genesis(self):
        genesis_block = Block(0, str(datetime.now()), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def add_block(self, img_hash):
        previous_hash = self.chain[-1].hash
        new_block = Block(len(self.chain), str(datetime.now()), img_hash, previous_hash)
        self.chain.append(new_block)


# Blockchain object
chain = Blockchain()



# steganography code

def encode():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
    if not path:
        return

    Img = Image.open(path)
    secretMessage = msg_entry.get()

    if secretMessage == "":
        messagebox.showwarning("Warning", "Please enter message to hide.")
        return

    # Perform Steganography
    steImg = stepic.encode(Img, secretMessage.encode())

    # Create output filename = originalName_encode.png
    base = os.path.splitext(os.path.basename(path))[0]
    output_file = base + "_encode.png"
    steImg.save(output_file)

    # Calculate hash of encoded image
    with open(output_file, "rb") as f:
        img_bytes = f.read()
        img_hash = hashlib.sha256(img_bytes).hexdigest()

    # Store hash only for the first encoded image
    if len(chain.chain) == 1:
        chain.add_block(img_hash)
        messagebox.showinfo("Success ", f"Message Hidden + Blockchain Hash Stored\nSaved as: {output_file}")
    else:
        messagebox.showinfo("Success ", f"Message Hidden\nSaved as: {output_file}\n(Blockchain unchanged)")


def decode():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
    if not path:
        return

    Img = Image.open(path)
    secretMessage = stepic.decode(Img).decode()
    messagebox.showinfo("Secret Message", f"Hidden Message:\n\n{secretMessage}")


def verify():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
    if not path:
        return

    # Calculate hash of selected image
    with open(path, "rb") as f:
        img_bytes = f.read()
        new_hash = hashlib.sha256(img_bytes).hexdigest()

    # Compare with blockchain stored hash
    for block in chain.chain:
        if block.data == new_hash:
            messagebox.showinfo("Verification Result ", "Image is ORIGINAL ✔")
            return

    messagebox.showwarning("Verification Result ", "Image is TAMPERED ")


# GUI
root = tk.Tk()
root.title('Blockchain-Based CryptoPix')
root.geometry("360x360")
root.configure(bg="#eed9b5")

title = tk.Label(root, text="CryptoPix + Blockchain", font=("Helvetica", 16, "bold"), fg="#4b1e00", bg="#eed9b5")
title.pack(pady=15)

msg_label = tk.Label(root, text="Enter Message to Hide:", font=("Arial", 12), bg="#eed9b5", fg="#4b1e00")
msg_label.pack()

msg_entry = tk.Entry(root, width=30, font=("Arial", 12))
msg_entry.pack(pady=5)

btn1 = tk.Button(root, text="Hide Message in Image", font=("Arial", 12), bg="#4b1e00", fg="#eed9b5", command=encode)
btn1.pack(pady=12, ipadx=10, ipady=5)

btn2 = tk.Button(root, text="Reveal Message", font=("Arial", 12), bg="#4b1e00", fg="#eed9b5", command=decode)
btn2.pack(pady=12, ipadx=10, ipady=5)

btn3 = tk.Button(root, text="Verify Image Authenticity", font=("Arial", 12), bg="#4b1e00", fg="#eed9b5", command=verify)
btn3.pack(pady=12, ipadx=10, ipady=5)

root.mainloop()
