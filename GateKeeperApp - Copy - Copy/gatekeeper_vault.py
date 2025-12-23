import os
import shutil

VAULT_DIR = "gatekeeper_vault"
CHAMBER_COUNT = 4
EMERGENCY_FLAG = os.path.join(VAULT_DIR, "EMERGENCY_SHUTDOWN")

def initialize_vault_structure():
    os.makedirs(VAULT_DIR, exist_ok=True)
    for i in range(1, CHAMBER_COUNT + 1):
        chamber_path = os.path.join(VAULT_DIR, f"chamber_{i}")
        os.makedirs(chamber_path, exist_ok=True)
import tkinter as tk
from tkinter import messagebox
import os

def open_vault_viewer(root, is_admin=True):
    BG_COLOR = "#1e1e2f"
    FG_COLOR = "#ffffff"
    BTN_COLOR = "#3a3a5c"
    ACCENT_COLOR = "#00d1b2"
    FONT = ("Consolas", 11)
    TITLE_FONT = ("Consolas", 16, "bold")
    VAULT_DIR = "gatekeeper_vault"

    viewer = tk.Toplevel(root)
    viewer.title("Vault Viewer"\)
    viewer.geometry("700x500")
    viewer.configure(bg=BG_COLOR)

    tk.Label(viewer, text="Stored Scripts", font=TITLE_FONT, fg=ACCENT_COLOR, bg=BG_COLOR).pack(pady=10)

    search_var = tk.StringVar()
    if is_admin:
        search_entry = tk.Entry(viewer, textvariable=search_var, font=FONT, bg=BTN_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR)
        search_entry.pack(pady=5)
        search_entry.insert(0, "Search...Gatekeeper ")

    listbox = tk.Listbox(viewer, font=FONT, bg=BTN_COLOR, fg=FG_COLOR, selectbackground=ACCENT_COLOR, width=80, height=15)
    listbox.pack(padx=20, pady=10)

    all_scripts = []
    for root_dir, _, files in os.walk(VAULT_DIR):
        for file in files:
            if file.endswith(".py"):
                rel_path = os.path.relpath(os.path.join(root_dir, file), VAULT_DIR)
                all_scripts.append(rel_path)

    def refresh_list(filter_text=""):
        listbox.delete(0, tk.END)
        for script in all_scripts:
            if filter_text.lower() in script.lower():
                listbox.insert(tk.END, script)

    refresh_list()

    def view_script():
        selected = listbox.get(tk.ACTIVE)
        if selected:
            full_path = os.path.join(VAULT_DIR, selected)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                content_window = tk.Toplevel(viewer)
                content_window.title(f"Viewing: {selected}")
                content_window.geometry("700x500")
                content_window.configure(bg=BG_COLOR)

                text = tk.Text(content_window, wrap="word", font=FONT, bg=BG_COLOR, fg=FG_COLOR, insertbackground=FG_COLOR)
                text.insert(tk.END, content)
                text.pack(expand=True, fill="both", padx=10, pady=10)
                text.config(state="disabled")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{e}")

    def delete_script():
        selected = listbox.get(tk.ACTIVE)
        if selected:
            full_path = os.path.join(VAULT_DIR, selected)
            confirm = messagebox.askyesno("Delete Script", f"Are you sure you want to delete:\n{selected}?")
            if confirm:
                try:
                    os.remove(full_path)
                    all_scripts.remove(selected)
                    refresh_list(search_var.get())
                    messagebox.showinfo("Deleted", f"{selected} has been deleted.")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not delete file:\n{e}")

    def copy_script():
        selected = listbox.get(tk.ACTIVE)
        if selected:
            full_path = os.path.join(VAULT_DIR, selected)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                viewer.clipboard_clear()
                viewer.clipboard_append(content)
                messagebox.showinfo("Copied", f"{selected} copied to clipboard.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not copy file:\n{e}")

    tk.Button(viewer, text="View Script", font=FONT, bg=BTN_COLOR, fg=FG_COLOR, command=view_script).pack(pady=5)

    if is_admin:
        admin_frame = tk.Frame(viewer, bg=BG_COLOR)
        admin_frame.pack(pady=5)

        tk.Button(admin_frame, text="Copy to Clipboard", font=FONT, bg=BTN_COLOR, fg=FG_COLOR, command=copy_script).grid(row=0, column=0, padx=5)
        tk.Button(admin_frame, text="Delete Script", font=FONT, bg=BTN_COLOR, fg=FG_COLOR, command=delete_script).grid(row=0, column=1, padx=5)

        def on_search(*args):
            refresh_list(search_var.get())

        search_var.trace_add("write", on_search)


def is_emergency_shutdown():
    return os.path.exists(EMERGENCY_FLAG)

def trigger_emergency_shutdown():
    with open(EMERGENCY_FLAG, "w") as f:
        f.write("Emergency shutdown triggered.")

def clear_emergency_shutdown():
    if os.path.exists(EMERGENCY_FLAG):
        os.remove(EMERGENCY_FLAG)

def basic_script_check(script_text):
    red_flags = ["os.system", "eval(", "exec(", "subprocess", "socket", "pickle", "input(", "open(", "import shutil"]
    return any(flag in script_text for flag in red_flags)

def store_script(file_path):
    if is_emergency_shutdown():
        return "⚠️ Emergency shutdown active. Uploads are disabled."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return f"❌ Failed to read file: {e}"

    if basic_script_check(content):
        trigger_emergency_shutdown()
        return "🚨 Suspicious code detected. Emergency shutdown triggered."

    # Choose chamber by hash
    chamber_index = hash(file_path) % CHAMBER_COUNT + 1
    chamber_path = os.path.join(VAULT_DIR, f"chamber_{chamber_index}")
    os.makedirs(chamber_path, exist_ok=True)

    filename = os.path.basename(file_path)
    dest_path = os.path.join(chamber_path, filename)

    try:
        shutil.copy(file_path, dest_path)
        return f"✅ Script stored in {os.path.relpath(dest_path, VAULT_DIR)}"
    except Exception as e:
        return f"❌ Failed to store script: {e}"