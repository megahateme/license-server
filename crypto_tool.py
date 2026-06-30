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
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if not file_path:
        return
    with open(file_path, "rb") as f:
        data = f.read()
    encrypted = cipher.encrypt(data)
    out_path = file_path + ".enc"
    with open(out_path, "wb") as f:
        f.write(encrypted)
    messagebox.showinfo("Готово", f"Выполнил:\n{out_path}")

def run_encrypted():
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if not file_path:
        return
    try:
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        decrypted = cipher.decrypt(encrypted_data)
        temp_dir = tempfile.gettempdir()
        base_name = os.path.basename(file_path)
        if base_name.endswith(".enc"):
            base_name = base_name[:-4]
        ext = os.path.splitext(base_name)[1]
        if ext.lower() == ".bat":
            temp_file = os.path.join(temp_dir, "temp_decrypted.bat")
            with open(temp_file, "wb") as f:
                f.write(decrypted)
            subprocess.Popen(["cmd", "/c", "start", temp_file])
        else:
            temp_file = os.path.join(temp_dir, "temp_decrypted.bin")
            with open(temp_file, "wb") as f:
                f.write(decrypted)
            os.startfile(temp_file)
        try:
            os.remove(file_path)
            messagebox.showinfo("Готово", f"Файл открыт\n.enc удалён")
        except:
            messagebox.showinfo("Готово", f"Файл открыт")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

# ====== GUI ======
root = tk.Tk()
root.title("Universal Encrypt Tool")
root.geometry("320x250")
root.resizable(False, False)

tk.Label(root, text="Universal Encrypt Tool", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="ТЫК (1)", command=encrypt_file, height=2, width=25).pack(pady=5)
tk.Button(root, text="ТЫК (2)", command=run_encrypted, height=2, width=25).pack(pady=5)
tk.Button(root, text="❌ Выход", command=root.quit, height=2, width=25).pack(pady=10)

root.mainloop()