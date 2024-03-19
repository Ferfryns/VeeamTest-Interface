import shutil
import os
import time
import tkinter as tk
from tkinter import filedialog

def perform_backup(source, destination):
    try:
        if os.path.exists(destination):
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            shutil.copytree(source, destination)
        print("Backup completed successfully!")
        return True
    except Exception as e:
        print(f"Error performing backup: {e}")
        return False

def create_log(message, log_path, log_level="INFO"):
    try:
        with open(log_path, "a") as log_file:
            log_file.write(f"{time.ctime()} [{log_level}] - {message}\n")
        print(f"[{log_level}] {message}")
    except Exception as e:
        print(f"Error creating log: {e}")

def perform_backup_and_log(source, destination, log_folder):
    log_path = os.path.join(log_folder, "backup_log.txt")
    if perform_backup(source, destination):
        create_log(f"Backup from {source} to {destination} completed successfully.", log_path)
    else:
        create_log(f"Failed to perform backup from {source} to {destination}.", log_path, "ERROR")

def run_backup(root, source, destination, frequency_minutes, log_folder):
    log_path = os.path.join(log_folder, "backup_log.txt")
    perform_backup_and_log(source, destination, log_folder)
    cleanup_destination(source, destination, log_folder)
    root.after(frequency_minutes * 60 * 1000, run_backup, root, source, destination, frequency_minutes, log_folder)

def cleanup_destination(source, destination, log_folder):
    try:
        for root_dir, dirs, files in os.walk(destination, topdown=False):
            for item in files:
                item_path = os.path.join(root_dir, item)
                relative_path = os.path.relpath(item_path, destination)
                source_item_path = os.path.join(source, relative_path)
                if not os.path.exists(source_item_path):
                    os.remove(item_path)
                    create_log(f"Removed file '{relative_path}' from the destination folder.", os.path.join(log_folder, "backup_log.txt"), "INFO")
            for item in dirs:
                item_path = os.path.join(root_dir, item)
                relative_path = os.path.relpath(item_path, destination)
                source_item_path = os.path.join(source, relative_path)
                if not os.path.exists(source_item_path):
                    shutil.rmtree(item_path)
                    create_log(f"Removed directory '{relative_path}' from the destination folder.", os.path.join(log_folder, "backup_log.txt"), "INFO")
    except Exception as e:
        create_log(f"Error cleaning up destination folder: {e}", os.path.join(log_folder, "backup_log.txt"), "ERROR")

def select_source(entry):
    source = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, source)

def select_destination(entry):
    destination = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, destination)

def select_log_folder(entry):
    log_folder = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, log_folder)

def main():
    root = tk.Tk()
    root.title("Veeam Synchronization Test Program")

    tk.Label(root, text="Source:").grid(row=0, column=0)
    source_entry = tk.Entry(root, width=50)
    source_entry.grid(row=0, column=1)
    tk.Button(root, text="Select Source", command=lambda: select_source(source_entry)).grid(row=0, column=2)

    tk.Label(root, text="Destination:").grid(row=1, column=0)
    destination_entry = tk.Entry(root, width=50)
    destination_entry.grid(row=1, column=1)
    tk.Button(root, text="Select Destination", command=lambda: select_destination(destination_entry)).grid(row=1, column=2)

    tk.Label(root, text="Log Folder:").grid(row=2, column=0)
    log_folder_entry = tk.Entry(root, width=50)
    log_folder_entry.grid(row=2, column=1)
    tk.Button(root, text="Select Log Folder", command=lambda: select_log_folder(log_folder_entry)).grid(row=2, column=2)

    tk.Label(root, text="Frequency (minutes):").grid(row=3, column=0)
    frequency_entry = tk.Entry(root)
    frequency_entry.grid(row=3, column=1)

    run_button = tk.Button(root, text="Start Backup", command=lambda: start_backup(root, source_entry, destination_entry, frequency_entry, log_folder_entry))
    run_button.grid(row=4, columnspan=3)

    root.mainloop()

def start_backup(root, source_entry, destination_entry, frequency_entry, log_folder_entry):
    source = source_entry.get()
    destination = destination_entry.get()
    frequency_minutes = int(frequency_entry.get())
    log_folder = log_folder_entry.get()

    run_backup(root, source, destination, frequency_minutes, log_folder)

if __name__ == "__main__":
    main()
