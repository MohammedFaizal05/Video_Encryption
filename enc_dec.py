import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
import pickle
import shutil

# GUI Setup
root = tk.Tk()
root.title("Video Encryption Decryption")
root.geometry("600x400")

# Select File Function
def select_file():
    global filename
    filename = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), ("Video Files", "*.mp4;*.avi")])
    if filename:
        lbl_file.config(text=f"Selected: {filename}")

def generate_key(shape):
    return np.random.randint(0, 256, shape, dtype=np.uint8)

def convert_avi_to_mp4(avi_path):
    mp4_path = avi_path.replace(".avi", ".mp4")
    clip = VideoFileClip(avi_path)
    clip.write_videofile(mp4_path, codec="libx264")
    clip.close()
    return mp4_path

# Encrypt Function
def encrypt_video():
    global filename
    if not filename:
        messagebox.showerror("Error", "No video selected!")
        return
    
    video_name = os.path.splitext(os.path.basename(filename))[0]
    results_folder = os.path.join(os.getcwd(), "Results")
    video_folder = os.path.join(results_folder, video_name)
    os.makedirs(video_folder, exist_ok=True)
    
    cap = cv2.VideoCapture(filename)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    encrypted_video_path = os.path.join(video_folder, "encrypted.avi")
    out = cv2.VideoWriter(encrypted_video_path, cv2.VideoWriter_fourcc(*'FFV1'), fps, (frame_width, frame_height))
    
    keys = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        key = generate_key(frame.shape)
        encrypted_frame = cv2.bitwise_xor(frame, key)  # XOR Encryption
        out.write(encrypted_frame)
        keys.append(key)
    
    cap.release()
    out.release()
    
    convert_avi_to_mp4(encrypted_video_path)
    
    # Save Key
    key_path = os.path.join(video_folder, "encryption_key.pkl")
    with open(key_path, "wb") as f:
        pickle.dump(keys, f)
    
    messagebox.showinfo("Success", f"Video Encrypted & Key Saved in {video_folder}!")

# Decrypt Function
def decrypt_video():
    global filename
    if not filename:
        messagebox.showerror("Error", "No video selected!")
        return
    
    video_name = os.path.splitext(os.path.basename(filename))[0]
    results_folder = os.path.join(os.getcwd(), "Results")
    video_folder = os.path.join(results_folder, video_name)
    encrypted_video_path = os.path.join(video_folder, "encrypted.avi")
    key_path = os.path.join(video_folder, "encryption_key.pkl")
    decrypted_video_path = os.path.join(video_folder, "decrypted.avi")
    
    if not os.path.exists(encrypted_video_path) or not os.path.exists(key_path):
        messagebox.showerror("Error", "No encrypted video or key found!")
        return
    
    cap = cv2.VideoCapture(encrypted_video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    with open(key_path, "rb") as f:
        keys = pickle.load(f)
    
    out = cv2.VideoWriter(decrypted_video_path, cv2.VideoWriter_fourcc(*'FFV1'), fps, (frame_width, frame_height))
    
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret or i >= len(keys):
            break
        
        decrypted_frame = cv2.bitwise_xor(frame, keys[i])  # XOR Decryption
        out.write(decrypted_frame)
        i += 1
    
    cap.release()
    out.release()
    
    convert_avi_to_mp4(decrypted_video_path)
    
    messagebox.showinfo("Success", f"Video Decrypted & Saved in {video_folder}!")

# UI Elements
lbl_file = tk.Label(root, text="Select a video", font=("Arial", 14))
lbl_file.pack(pady=10)

btn_select = tk.Button(root, text="Select Video", command=select_file, font=("Arial", 12))
btn_select.pack(pady=5)

btn_encrypt = tk.Button(root, text="Encrypt Video", command=encrypt_video, font=("Arial", 12), bg="orange")
btn_encrypt.pack(pady=5)

btn_decrypt = tk.Button(root, text="Decrypt Video", command=decrypt_video, font=("Arial", 12), bg="green")
btn_decrypt.pack(pady=5)

root.mainloop()
            