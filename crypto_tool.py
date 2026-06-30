import os
import tempfile
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet

KEY_FILE = "key.key"

def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

cipher = Fernet(load_or_create_key())

def encrypt_file():
    file_path = filedialog.askopenfilename(filetypes=[("EXE files", "*.exe")])
    if not file_path:
        return
    with open(file_path, "rb") as f:
        data = f.read()
    encrypted = cipher.encrypt(data)
    out_path = file_path + ".enc"
    with open(out_path, "wb") as f:
        f.write(encrypted)
    messagebox.showinfo("Готово", f"Зашифровано:\n{out_path}")

def run_encrypted():
    file_path = filedialog.askopenfilename(filetypes=[("ENC files", "*.enc")])
    if not file_path:
        return
    try:
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        decrypted = cipher.decrypt(encrypted_data)
        temp_dir = tempfile.gettempdir()
        temp_exe = os.path.join(temp_dir, "temp_run.exe")
        with open(temp_exe, "wb") as f:
            f.write(decrypted)
        subprocess.Popen(temp_exe)
        messagebox.showinfo("Готово", "Программа запущена")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

# GUI
root = tk.Tk()
root.title("EXE Encrypt Tool")
root.geometry("320x250")
root.resizable(False, False)

tk.Label(root, text="EXE Encrypt Tool", font=("Arial", 14, "bold")).pack(pady=10)

# ===== КНОПКИ С НОВЫМИ НАЗВАНИЯМИ =====
tk.Button(root, text="ТЫК (1)", command=encrypt_file, height=2, width=25).pack(pady=5)
tk.Button(root, text="ТЫК (2)", command=run_encrypted, height=2, width=25).pack(pady=5)
tk.Button(root, text="❌ Выход", command=root.quit, height=2, width=25).pack(pady=10)

root.mainloop()