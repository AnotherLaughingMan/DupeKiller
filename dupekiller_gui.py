import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from PIL import Image, ImageTk
import time

def show_splash(duration=3000):
    hidden_root = tk.Tk()
    hidden_root.withdraw()  # Hide the root window

    splash = tk.Toplevel(hidden_root)
    splash.overrideredirect(True)
    splash.configure(bg='black')

    try:
        img = Image.open("splash.png")
        splash_img = ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading splash image: {e}")
        splash.destroy()
        hidden_root.destroy()
        return

    width, height = img.size
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    splash.geometry(f"{width}x{height}+{x}+{y}")

    canvas = tk.Canvas(splash, width=width, height=height, highlightthickness=0)
    canvas.pack()
    canvas.create_image(0, 0, anchor='nw', image=splash_img)

    splash.after(duration, lambda: (splash.destroy(), hidden_root.destroy()))
    splash.mainloop()

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)

def find_name_duplicates(folder):
    duplicates = []
    for root_dir, _, files in os.walk(folder):
        for name in files:
            if " - Copy" in name:
                filepath = os.path.join(root_dir, name)
                duplicates.append(filepath)
    return duplicates

def preview_duplicates():
    folder = folder_entry.get()
    if not folder:
        messagebox.showwarning("No Folder Selected", "Please select a folder first.")
        return

    global current_duplicates
    current_duplicates = find_name_duplicates(folder)

    preview_text.delete(1.0, tk.END)
    preview_text.insert(tk.END, f"Previewing duplicates in: {folder}\n\n", "summary")
    for file in current_duplicates:
        preview_text.insert(tk.END, file + "\n")

    counter_label.config(text=f"Duplicate files found: {len(current_duplicates)}")
    delete_count_label.config(text=f"{len(current_duplicates)} files")

def delete_duplicates():
    if not current_duplicates:
        messagebox.showinfo("No Duplicates", "No duplicates to delete.")
        return

    dry_run = dry_run_var.get()
    mode_text = "simulate deletion of" if dry_run else "delete"
    confirm = messagebox.askyesno("Confirm Action", f"Are you sure you want to {mode_text} {len(current_duplicates)} files?")
    if not confirm:
        return

    deleted = 0
    deleted_files = []

    preview_text.delete(1.0, tk.END)
    preview_text.insert(tk.END, f"{'Dry-Run: Simulating' if dry_run else 'Deleting'} {len(current_duplicates)} files:\n\n", "summary")

    for file in current_duplicates:
        try:
            if not dry_run:
                os.remove(file)
            deleted_files.append(file)
            tag = "dryrun" if dry_run else "deleted"
            preview_text.insert(tk.END, file + "\n", tag)
            deleted += 1
        except Exception as e:
            print(f"Error deleting {file}: {e}")

    app_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"dupekiller_log_{timestamp}.txt"
    log_path = os.path.join(app_dir, log_filename)

    try:
        with open(log_path, "w") as log:
            log.write(f"Dupe Killer Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log.write(f"{'Dry-Run: Simulated deletion of' if dry_run else 'Deleted'} {deleted} files:\n\n")
            for file in deleted_files:
                log.write(file + "\n")
    except Exception as e:
        print(f"Error writing log file: {e}")

    if auto_open_var.get():
        try:
            if os.name == 'nt':
                os.startfile(log_path)
            elif os.name == 'posix':
                import subprocess
                subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', log_path])
        except Exception as e:
            print(f"Error opening log file: {e}")

    messagebox.showinfo("Action Complete", f"{deleted} files {'simulated' if dry_run else 'deleted'}.\nLog saved to:\n{log_path}")
    counter_label.config(text=f"{'Simulated' if dry_run else 'Deleted'}: {deleted} files")
    delete_count_label.config(text=f"{deleted} files")

# Show splash screen before launching main GUI
show_splash(duration=3000)

# Initialize main window
root = tk.Tk()
root.title("Dupe Killer v1.1 by AnotherLaughingMan")
root.geometry("750x580")
root.minsize(750, 580)

content_frame = tk.Frame(root)
content_frame.pack(fill=tk.BOTH, expand=True)

folder_frame = tk.Frame(content_frame)
folder_frame.pack(pady=5)
folder_entry = tk.Entry(folder_frame, width=60)
folder_entry.pack(side=tk.LEFT, padx=5)
browse_button = tk.Button(folder_frame, text="Browse", command=browse_folder)
browse_button.pack(side=tk.LEFT)

button_frame = tk.Frame(content_frame)
button_frame.pack(pady=5)

preview_button = tk.Button(button_frame, text="Preview Duplicates", command=preview_duplicates)
preview_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(button_frame, text="Delete Duplicates", command=delete_duplicates)
delete_button.pack(side=tk.LEFT, padx=5)

delete_count_label = tk.Label(button_frame, text="0 files", font=("Helvetica", 10))
delete_count_label.pack(side=tk.LEFT, padx=10)

dry_run_var = tk.BooleanVar()
dry_run_checkbox = tk.Checkbutton(button_frame, text="Dry-Run Mode (Preview Only)", variable=dry_run_var)
dry_run_checkbox.pack(side=tk.LEFT, padx=10)

auto_open_var = tk.BooleanVar()
auto_open_checkbox = tk.Checkbutton(button_frame, text="Auto-Open Log After Deletion", variable=auto_open_var)
auto_open_checkbox.pack(side=tk.LEFT, padx=10)

preview_frame = tk.Frame(content_frame)
preview_frame.pack(padx=10, pady=(10, 0), fill=tk.BOTH, expand=True)

x_scroll = tk.Scrollbar(preview_frame, orient=tk.HORIZONTAL)
x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

y_scroll = tk.Scrollbar(preview_frame)
y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

preview_text = tk.Text(preview_frame, wrap=tk.NONE, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

x_scroll.config(command=preview_text.xview)
y_scroll.config(command=preview_text.yview)

preview_text.tag_config("dryrun", foreground="orange")
preview_text.tag_config("deleted", foreground="red")
preview_text.tag_config("summary", foreground="blue", font=("Helvetica", 10, "bold"))

footer_frame = tk.Frame(root)
footer_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

version_label = tk.Label(footer_frame, text="Version 1.1", anchor="w", font=("Helvetica", 9), fg="gray")
version_label.pack(side=tk.LEFT)

counter_label = tk.Label(footer_frame, text="Duplicate files found: 0", anchor="e", font=("Helvetica", 10))
counter_label.pack(side=tk.RIGHT)

current_duplicates = []

root.mainloop()
