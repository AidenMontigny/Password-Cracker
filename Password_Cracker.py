import hashlib
import bcrypt
import itertools
import string
import logging
import os
import tkinter as tk
from tkinter import messagebox
import threading 
from tkinter import ttk

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def hash_md5(password):
    return hashlib.md5(password.encode()).hexdigest()

def hash_sha256(password):
    return hashlib.sha256(password.encode()).hexdigest()

def hash_bcrypt(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def brute_force_attack(target_hash, algorithm, length=4, chars=None, progress_callback=None):
    if chars is None:
        chars = string.ascii_lowercase + string.digits  
    total_combinations = len(chars) ** length
    count = 0

    for password_tuple in itertools.product(chars, repeat=length):
        password = ''.join(password_tuple)
        count += 1
        if algorithm == hash_bcrypt:
            if bcrypt.checkpw(password.encode(), target_hash.encode()):
                return password
        else:
            hashed_password = algorithm(password)
            if hashed_password == target_hash:
                return password

        if progress_callback:
            progress_callback(count / total_combinations)

    return None

def dictionary_attack(target_hash, algorithm, dictionary_file, progress_callback=None):
    if not os.path.exists(dictionary_file):
        logging.error(f"Dictionary file '{dictionary_file}' not found.")
        return None
    try:
        with open(dictionary_file, 'r') as file:
            total_lines = sum(1 for line in file)  
            count = 0

            for line in file:
                password = line.strip()
                count += 1
                if algorithm == hash_bcrypt:
                    if bcrypt.checkpw(password.encode(), target_hash.encode()):
                        return password
                else:
                    hashed_password = algorithm(password)
                    if hashed_password == target_hash:
                        return password

                if progress_callback:
                    progress_callback(count / total_lines)
    except Exception as e:
        logging.error(f"Error reading dictionary file: {e}")
    return None

def start_cracking(selected_algorithm):
    def run_cracking():
        original_password = "password123" 

        algorithms = {
            "md5": hash_md5,
            "sha256": hash_sha256,
            "bcrypt": hash_bcrypt
        }

        if selected_algorithm not in algorithms:
            messagebox.showerror("Error", "Invalid algorithm selected.")
            return

        hash_algorithm = algorithms[selected_algorithm]
        
        target_hash = hash_algorithm(original_password)
        messagebox.showinfo("Hashed Password", f"Original password: {original_password}\nHashed password: {target_hash}")

        progress_var.set(0)
        progress_bar.pack(pady=20)

        cracked_password = brute_force_attack(target_hash, hash_algorithm, length=4, progress_callback=update_progress)
        if cracked_password:
            messagebox.showinfo("Brute Force Attack", f"Password cracked with brute force: {cracked_password}")
        else:
            messagebox.showinfo("Brute Force Attack", "Brute force failed")

        dictionary_file = 'C:\\Users\\aiden\\source\\repos\\Password Cracker\\dictionary.txt'
        cracked_password = dictionary_attack(target_hash, hash_algorithm, dictionary_file, progress_callback=update_progress)
        if cracked_password:
            messagebox.showinfo("Dictionary Attack", f"Password cracked with dictionary attack: {cracked_password}")
        else:
            messagebox.showinfo("Dictionary Attack", "Dictionary attack failed")

        progress_bar.pack_forget()  

    thread = threading.Thread(target=run_cracking)
    thread.start()

def update_progress(progress):
    progress_var.set(progress)
    window.update_idletasks() 

def create_gui():
    global window, progress_var, progress_bar

    window = tk.Tk()
    window.title("Password Cracker")

    window.geometry("400x400")  

    label = tk.Label(window, text="Select a hashing algorithm", font=("Arial", 14))
    label.pack(pady=20)

    btn_md5 = tk.Button(window, text="MD5", font=("Arial", 12), command=lambda: start_cracking("md5"))
    btn_md5.pack(pady=10, padx=20, fill='x')

    btn_sha256 = tk.Button(window, text="SHA256", font=("Arial", 12), command=lambda: start_cracking("sha256"))
    btn_sha256.pack(pady=10, padx=20, fill='x')

    btn_bcrypt = tk.Button(window, text="bcrypt", font=("Arial", 12), command=lambda: start_cracking("bcrypt"))
    btn_bcrypt.pack(pady=10, padx=20, fill='x')

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(window, variable=progress_var, maximum=1, length=300)
    
    window.mainloop()

if __name__ == "__main__":
    create_gui()
