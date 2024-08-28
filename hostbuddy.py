import os
import subprocess
import re
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Scrollbar, Text

# Function to backup hosts file
def backup_hosts_file(hosts_file):
    backup_file = hosts_file + ".bak"
    try:
        subprocess.run(["sudo", "cp", hosts_file, backup_file], check=True)
        log_message(f"Backup created successfully at {backup_file}.")
    except subprocess.CalledProcessError as e:
        log_message(f"Error creating backup: {e}")
        return False
    return True

# Function to validate IP address
def is_valid_ip(ip):
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return pattern.match(ip) is not None

# Function to validate hostname
def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]
    allowed = re.compile(r"^(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

# Function to add/update hosts entry
def update_hosts_file():
    ip_address = ip_entry.get()
    host_name = host_entry.get()
    hosts_file = file_path.get()

    if not ip_address or not host_name:
        messagebox.showerror("Input Error", "Both IP address and hostname are required.")
        return

    if not is_valid_ip(ip_address):
        messagebox.showerror("Input Error", "Invalid IP address format.")
        return

    if not is_valid_hostname(host_name):
        messagebox.showerror("Input Error", "Invalid hostname format.")
        return

    if not backup_hosts_file(hosts_file):
        return
    
    try:
        with open(hosts_file, "r+") as file:
            lines = file.readlines()
            found = False
            for i, line in enumerate(lines):
                if host_name in line:
                    lines[i] = f"{ip_address}\t{host_name}\n"
                    found = True
                    break
            if not found:
                lines.append(f"{ip_address}\t{host_name}\n")
            file.seek(0)
            file.writelines(lines)
            file.truncate()
        log_message(f"Updated {host_name} to {ip_address} in {hosts_file}.")
    except Exception as e:
        log_message(f"Error updating hosts file: {e}")

# Function to remove hosts entry
def remove_hosts_entry():
    host_name = host_entry.get()
    hosts_file = file_path.get()

    if not host_name:
        messagebox.showerror("Input Error", "Hostname is required.")
        return

    if not backup_hosts_file(hosts_file):
        return
    
    try:
        with open(hosts_file, "r+") as file:
            lines = file.readlines()
            lines = [line for line in lines if host_name not in line]
            file.seek(0)
            file.writelines(lines)
            file.truncate()
        log_message(f"Removed {host_name} from {hosts_file}.")
    except Exception as e:
        log_message(f"Error removing hosts entry: {e}")

# Function to restore from backup
def restore_from_backup():
    hosts_file = file_path.get()
    backup_file = hosts_file + ".bak"

    if not os.path.exists(backup_file):
        messagebox.showerror("Backup Error", f"No backup found at {backup_file}.")
        return

    try:
        subprocess.run(["sudo", "cp", backup_file, hosts_file], check=True)
        log_message(f"Restored {hosts_file} from {backup_file}.")
    except subprocess.CalledProcessError as e:
        log_message(f"Error restoring from backup: {e}")

# Function to log messages in the GUI
def log_message(message):
    log_text.insert(tk.END, message + "\n")
    log_text.yview(tk.END)

# Function to select a hosts file
def select_hosts_file():
    selected_file = filedialog.askopenfilename(initialdir="/etc", title="Select hosts file", filetypes=(("Hosts files", "*.hosts"), ("All files", "*.*")))
    if selected_file:
        file_path.set(selected_file)

# Function to clear input fields
def clear_fields():
    ip_entry.delete(0, tk.END)
    host_entry.delete(0, tk.END)

# Function to display the current hosts file in a popup window
def preview_hosts_file():
    hosts_file = file_path.get()
    
    try:
        with open(hosts_file, "r") as file:
            content = file.read()
            
        # Create a new popup window
        preview_window = Toplevel(root)
        preview_window.title("Preview of Hosts File")
        
        # Add a scrollable text area to display the content
        text_area = Text(preview_window, wrap=tk.NONE)
        text_area.insert(tk.END, content)
        text_area.configure(state='disabled')  # Make the text area read-only
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add a scrollbar
        scrollbar = Scrollbar(preview_window, orient=tk.VERTICAL, command=text_area.yview)
        text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load hosts file: {e}")

# GUI setup
root = tk.Tk()
root.title("Hosts File Editor")

# Restrict resizing of the window
root.resizable(False, False)

# File path selection
tk.Label(root, text="Hosts File:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
file_path = tk.StringVar(value="/etc/hosts")
tk.Entry(root, textvariable=file_path, width=40).grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=select_hosts_file).grid(row=0, column=2, padx=5, pady=5)

# IP Address input
tk.Label(root, text="IP Address:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
ip_entry = tk.Entry(root)
ip_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='we')

# Hostname input
tk.Label(root, text="Hostname:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
host_entry = tk.Entry(root)
host_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='we')

# Add/Update button
tk.Button(root, text="Add/Update Entry", command=update_hosts_file).grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='we')

# Clear fields button
tk.Button(root, text="Clear", command=clear_fields).grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky='we')

# Remove entry button
tk.Button(root, text="Remove Entry", command=remove_hosts_entry).grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky='we')

# Restore from backup button
tk.Button(root, text="Restore from Backup", command=restore_from_backup).grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky='we')

# Preview hosts file button
tk.Button(root, text="Preview Hosts File", command=preview_hosts_file).grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky='we')

# Log area
log_text = tk.Text(root, height=10, width=50)
log_text.grid(row=8, column=0, columnspan=3, padx=5, pady=5)

# Exit button
tk.Button(root, text="Exit", command=root.quit).grid(row=9, column=0, columnspan=3, padx=5, pady=5, sticky='we')

root.mainloop()

