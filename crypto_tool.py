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
    # ТЕПЕРЬ МОЖНО ВЫБРАТЬ ЛЮБОЙ ФАЙЛ
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
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
    # ПРИ РАСШИФРОВКЕ ТОЖЕ ЛЮБОЙ
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if not file_path:
        return
    try:
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        decrypted = cipher.decrypt(encrypted_data)
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, "temp_decrypted.bin")
        with open(temp_file, "wb") as f:
            f.write(decrypted)
        subprocess.Popen(temp_file)
        messagebox.showinfo("Готово", "Файл запущен")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

# GUI
root = tk.Tk()
root.title("Universal Encrypt Tool")
root.geometry("320x250")
root.resizable(False, False)

tk.Label(root, text="Universal Encrypt Tool", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="ТЫК (1)", command=encrypt_file, height=2, width=25).pack(pady=5)
tk.Button(root, text="ТЫК (2)", command=run_encrypted, height=2, width=25).pack(pady=5)
tk.Button(root, text="❌ Выход", command=root.quit, height=2, width=25).pack(pady=10)

root.mainloop()