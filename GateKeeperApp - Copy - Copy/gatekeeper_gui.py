import tkinter as tk
from tkinter import filedialog, messagebox
import os
from gatekeeper_vault import (
    initialize_vault_structure,
    store_script,
    open_vault_viewer,
    is_emergency_shutdown,
    clear_emergency_shutdown,
)

# === Theme Settings ===
BG_COLOR = "#1e1e2f"
FG_COLOR = "#ffffff"
BTN_COLOR = "#3a3a5c"
ACCENT_COLOR = "#00d1b2"
FONT = ("Consolas", 11)
TITLE_FONT = ("Consolas", 16, "bold")

# === Admin Toggle ===
IS_ADMIN = True  # Set to False to hide admin features

# === GUI Setup ===
root = tk.Tk()
root.title("Gatekeeper Vault")
root.geometry("500x300")
root.configure(bg=BG_COLOR)

# === Vault Setup ===
if not os.path.exists("gatekeeper_vault"):
    initialize_vault_structure()

# === Functions ===
def upload_and_scan():
    if is_emergency_shutdown():
        messagebox.showwarning("Emergency Shutdown", "Uploads are disabled due to a previous threat.")
        return

    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        result = store_script(file_path)
        messagebox.showinfo("Scan Result", result)

def show_about():
    messagebox.showinfo("About Gatekeeper", "Gatekeeper Vault\nVersion 1.0\nBuilt to protect your system from malicious scripts.")

def reset_emergency():
    if is_emergency_shutdown():
        confirm = messagebox.askyesno("Reset Emergency", "Clear emergency shutdown and resume uploads?")
        if confirm:
            clear_emergency_shutdown()
            messagebox.showinfo("Reset", "Emergency shutdown cleared.")
    else:
        messagebox.showinfo("Status", "No emergency shutdown is active.")

# === Layout ===
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(padx=20, pady=20)

tk.Label(main_frame, text="Gatekeeper Vault", font=TITLE_FONT, fg=ACCENT_COLOR, bg=BG_COLOR).grid(row=0, column=0, columnspan=2, pady=10)

tk.Button(main_frame, text="Upload & Scan", font=FONT, bg=BTN_COLOR, fg=FG_COLOR, command=upload_and_scan).grid(row=1, column=0, padx=10, pady=10)
tk.Button(main_frame, text="Open Vault Viewer", font=FONT, bg=BTN_COLOR, fg=FG_COLOR, command=lambda: open_vault_viewer(root, IS_ADMIN)).grid(row=1, column=1, padx=10, pady=10)
tk.Button(main_frame, text="About Gatekeeper", font=FONT, bg=BTN_COLOR, fg=FG_COLOR, command=show_about).grid(row=2, column=0, columnspan=2, pady=10)

if IS_ADMIN:
    tk.Button(main_frame, text="Reset Emergency", font=FONT, bg=BTN_COLOR, fg=FG_COLOR, command=reset_emergency).grid(row=3, column=0, columnspan=2, pady=5)

# === Run App ===
root.mainloop()