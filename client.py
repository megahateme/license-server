import requests
import subprocess
import os
import sys
import tempfile
import shutil
import json
import tkinter as tk
from tkinter import messagebox

# ======== НАСТРОЙКИ ========
SERVER_URL = "https://license-server-q7pe.onrender.com/check"
LICENSE_FILE = "license.dat"

# ======== HWID ========
def get_hwid():
    try:
        result = subprocess.run(["wmic", "cpu", "get", "ProcessorId"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")
        if len(lines) > 1:
            return lines[1].strip()
    except:
        pass
    return "PC-12345"

# ======== РАБОТА С ЛИЦЕНЗИЕЙ (СОХРАНЕНИЕ) ========
def save_license(token, hwid):
    data = {
        "token": token,
        "hwid": hwid
    }
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f)

def load_license():
    if not os.path.exists(LICENSE_FILE):
        return None
    try:
        with open(LICENSE_FILE, "r") as f:
            return json.load(f)
    except:
        return None

def is_license_valid():
    data = load_license()
    if not data:
        return False
    current_hwid = get_hwid()
    if data.get("hwid") != current_hwid:
        return False
    return True

# ======== ЗАПУСК CRYPTO_TOOL ========
def run_crypto_tool():
    temp_dir = tempfile.gettempdir()
    crypto_exe = os.path.join(temp_dir, "crypto_tool.exe")
    
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
        source = os.path.join(bundle_dir, "crypto_tool.exe")
    else:
        source = "crypto_tool.exe"
    
    if not os.path.exists(source):
        messagebox.showerror("Ошибка", "crypto_tool.exe не найден!")
        return False
    
    shutil.copy2(source, crypto_exe)
    subprocess.Popen([crypto_exe])
    return True

# ======== ПРОВЕРКА КЛЮЧА ========
def check_license():
    key = entry_key.get().strip()
    if not key:
        messagebox.showerror("Ошибка", "Введите лицензионный ключ!")
        return
    
    hwid = get_hwid()
    status_label.config(text="⏳ Проверка ключа...")
    root.update()
    
    try:
        response = requests.post(SERVER_URL, json={"key": key, "hwid": hwid}, timeout=10)
        data = response.json()
    except:
        status_label.config(text="❌ Ошибка подключения к серверу")
        messagebox.showerror("Ошибка", "Не удалось подключиться к серверу")
        return
    
    if data.get("status") == "ok":
        # СОХРАНЯЕМ ЛИЦЕНЗИЮ
        save_license(data.get("token"), hwid)
        status_label.config(text="✅ Лицензия активирована!")
        root.after(500, lambda: close_and_run())
    else:
        status_label.config(text="❌ " + data.get("message", "Ошибка"))
        messagebox.showerror("Ошибка", data.get("message", "Неизвестная ошибка"))

def close_and_run():
    root.destroy()
    run_crypto_tool()

# ======== ОСНОВНАЯ ЛОГИКА ========
def main():
    global root, entry_key, status_label

    # ПРОВЕРЯЕМ, ЕСТЬ ЛИ УЖЕ СОХРАНЁННАЯ ЛИЦЕНЗИЯ
    if is_license_valid():
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Лицензия", "✅ Лицензия уже активирована!")
        run_crypto_tool()
        return

    # ЕСЛИ НЕТ — ПОКАЗЫВАЕМ ОКНО АКТИВАЦИИ
    root = tk.Tk()
    root.title("Активация лицензии")
    root.geometry("400x250")
    root.resizable(False, False)

    tk.Label(root, text="🔐 АКТИВАЦИЯ ЛИЦЕНЗИИ", font=("Arial", 16, "bold")).pack(pady=15)
    tk.Label(root, text="Введите лицензионный ключ:", font=("Arial", 10)).pack()

    entry_key = tk.Entry(root, width=35, font=("Arial", 12))
    entry_key.pack(pady=10)

    btn_check = tk.Button(root, text="✅ Активировать", command=check_license, height=2, width=20, bg="#4CAF50", fg="white")
    btn_check.pack(pady=10)

    status_label = tk.Label(root, text="", font=("Arial", 10))
    status_label.pack(pady=10)

    tk.Label(root, text="© License Server", font=("Arial", 8), fg="gray").pack(side="bottom", pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()