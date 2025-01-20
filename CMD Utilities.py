import tkinter as tk
import subprocess
import os
import json
import keyboard

# Function to get the current user's username
def get_user_name():
    return os.getlogin()

# Utility functions
def execute_command(command, force=False):
    try:
        # If 'force' is true, append the /f flag to the command
        if force:
            command = f"{command} /f"
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output_text.set(f"Command executed successfully:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        output_text.set(f"Error executing command:\n{e.stderr}")

def clear_screen():
    execute_command("cls")  # Clear the command line screen

def check_disk():
    # This function checks the disk for errors by running CHKDSK
    subprocess.Popen(["powershell", "-Command", "Start-Process cmd -ArgumentList '/c chkdsk C: /f' -Verb runAs"])

def shutdown_computer(force=False):
    # Shutdown the computer, with an option to force it
    if force:
        execute_command("shutdown /s /f /t 0")  # Force shutdown
    else:
        execute_command("shutdown /s /t 0")  # Normal shutdown

def restart_computer(force=False):
    # Restart the computer, with an option to force it
    if force:
        execute_command("shutdown /r /f /t 0")  # Force restart
    else:
        execute_command("shutdown /r /t 0")  # Normal restart

def run_sfc():
    # This function runs the System File Checker
    subprocess.Popen(["powershell", "-Command", "Start-Process cmd -ArgumentList '/c sfc /scannow' -Verb runAs"])

def defrag_disk():
    # This function defragments the disk
    subprocess.Popen(["powershell", "-Command", "Start-Process cmd -ArgumentList '/c defrag C:' -Verb runAs"])

def open_msconfig():
    # Open the System Configuration utility
    execute_command("msconfig")

def nslookup():
    # Run a DNS query
    execute_command("nslookup")

def show_version():
    # Show the Windows version
    execute_command("ver")

def clean_temp_files():
    # Delete temporary files
    execute_command("del /q /f /s %temp%\\*")

def save_shortcuts():
    # Save keyboard shortcuts to a JSON file
    shortcuts = {
        "shutdown": shutdown_shortcut_var.get(),
        "restart": restart_shortcut_var.get(),
    }
    with open("CMD_Utilities.json", "w") as f:
        json.dump(shortcuts, f)

def load_shortcuts():
    # Load keyboard shortcuts from the JSON file
    if os.path.exists("CMD_Utilities.json"):
        with open("CMD_Utilities.json", "r") as f:
            shortcuts = json.load(f)
            shutdown_shortcut_var.set(shortcuts.get("shutdown", ""))
            restart_shortcut_var.set(shortcuts.get("restart", ""))
            # Attach the shortcuts to their functions
            if shortcuts.get("shutdown"):
                keyboard.add_hotkey(shortcuts["shutdown"], lambda: shutdown_computer())
            if shortcuts.get("restart"):
                keyboard.add_hotkey(shortcuts["restart"], lambda: restart_computer())

# Browser Manager Functions
def check_browser_installed(browser_name):
    user_name = get_user_name()
    paths = []
    # Define paths for each browser executable
    if browser_name == "Brave":
        paths = [
            fr"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            fr"C:\Users\{user_name}\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"
        ]
    elif browser_name == "Opera":
        paths = [
            fr"C:\Program Files\Opera\opera.exe",
            fr"C:\Users\{user_name}\AppData\Local\Programs\Opera\opera.exe"
        ]
    elif browser_name == "Google Chrome":
        paths = [
            fr"C:\Program Files\Google\Chrome\Application\chrome.exe",
            fr"C:\Users\{user_name}\AppData\Local\Google\Chrome\Application\chrome.exe"
        ]
    elif browser_name == "Mozilla Firefox":
        paths = [
            fr"C:\Program Files\Mozilla Firefox\firefox.exe",
            fr"C:\Users\{user_name}\AppData\Local\Mozilla Firefox\firefox.exe"
        ]
    elif browser_name == "Microsoft Edge":
        paths = [
            fr"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            fr"C:\Users\{user_name}\AppData\Local\Microsoft\Edge\Application\msedge.exe"
        ]
    elif browser_name == "Vivaldi":
        paths = [
            fr"C:\Program Files\Vivaldi\Application\vivaldi.exe",
            fr"C:\Users\{user_name}\AppData\Local\Vivaldi\Application\vivaldi.exe"
        ]
    elif browser_name == "Internet Explorer":
        paths = [
            fr"C:\Program Files\Internet Explorer\iexplore.exe",
            fr"C:\Program Files (x86)\Internet Explorer\iexplore.exe"
        ]
    for path in paths:
        if os.path.exists(path):  # Check if the browser is installed
            return True
    return False

def install_browser(browser_name):
    # Install the specified browser using the Windows Package Manager
    try:
        result = subprocess.run(['winget', 'install', browser_name], check=True)
        output_text.set(f"{browser_name} has been installed successfully!")
    except subprocess.CalledProcessError:
        output_text.set(f"An error occurred while installing {browser_name}.")
    update_browser_status()

def uninstall_browser(browser_name):
    # Uninstall the specified browser using the Windows Package Manager
    try:
        result = subprocess.run(['winget', 'uninstall', browser_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "successfully uninstalled" in result.stdout.lower() or "disinstallato correttamente" in result.stdout.lower():
            output_text.set(f"{browser_name} has been uninstalled successfully!")
        else:
            output_text.set(f"Unknown error in uninstalling {browser_name}.")
    except subprocess.CalledProcessError:
        output_text.set(f"Error while uninstalling {browser_name}.")
    update_browser_status()

def update_browser_status():
    # Update the UI showing if the browsers are installed or not
    for browser_name, status_label, uninstall_button in browser_controls:
        if check_browser_installed(browser_name):  # If the browser is installed
            status_label.config(text="✔", fg="green")
            uninstall_button.config(state="normal")
        else:
            status_label.config(text="✘", fg="red")
            uninstall_button.config(state="disabled")

# Create the main window
root = tk.Tk()
root.title("CMD Utilities")  # Title of the application
root.geometry("800x600")  # Window size
root.configure(bg="#f0f0f0")  # Light background color

# --- System Tools Panel ---
tools_frame = tk.LabelFrame(root, text="System Tools", bg="#e0e0e0", padx=10, pady=10)
tools_frame.pack(pady=10, fill="both", side="left", expand=True)

instructions_label_tools = tk.Label(tools_frame, text="Select the command to execute:", bg="#e0e0e0")
instructions_label_tools.pack(pady=10)

# Variables to manage shortcuts
shutdown_shortcut_var = tk.StringVar()
restart_shortcut_var = tk.StringVar()

force_shutdown_var = tk.BooleanVar(value=True)  # Default to true for forced shutdown
force_restart_var = tk.BooleanVar(value=True)    # Default to true for forced restart

# Buttons for system commands
button_clear = tk.Button(tools_frame, text="CLS - Clear Screen", command=clear_screen, bg="#4caf50", fg="white", width=30)
button_clear.pack(pady=5)

button_chkdsk = tk.Button(tools_frame, text="CHKDSK - Check Disk", command=check_disk, bg="#2196f3", fg="white", width=30)
button_chkdsk.pack(pady=5)

frame_shutdown = tk.Frame(tools_frame, bg="#e0e0e0")
frame_shutdown.pack(pady=5)
shutdown_button = tk.Button(frame_shutdown, text="Shutdown", command=lambda: shutdown_computer(force=force_shutdown_var.get()), bg="#f44336", fg="white")
shutdown_button.pack(side="left", padx=10)

force_shutdown_checkbox = tk.Checkbutton(frame_shutdown, text="Force Shutdown", variable=force_shutdown_var, bg="#e0e0e0")
force_shutdown_checkbox.pack(side="left", padx=10)

frame_shutdown_shortcut = tk.Frame(tools_frame, bg="#e0e0e0")
frame_shutdown_shortcut.pack(pady=5)
shutdown_shortcut_entry = tk.Entry(frame_shutdown_shortcut, textvariable=shutdown_shortcut_var, width=15)
shutdown_shortcut_entry.pack(side="left", padx=10)
set_shutdown_key_button = tk.Button(frame_shutdown_shortcut, text="Set Key", command=save_shortcuts, bg="#ff9800", fg="white")
set_shutdown_key_button.pack(side="left")

frame_restart = tk.Frame(tools_frame, bg="#e0e0e0")
frame_restart.pack(pady=5)
restart_button = tk.Button(frame_restart, text="Restart", command=lambda: restart_computer(force=force_restart_var.get()), bg="#f44336", fg="white")
restart_button.pack(side="left", padx=10)

force_restart_checkbox = tk.Checkbutton(frame_restart, text="Force Restart", variable=force_restart_var, bg="#e0e0e0")
force_restart_checkbox.pack(side="left", padx=10)

frame_restart_shortcut = tk.Frame(tools_frame, bg="#e0e0e0")
frame_restart_shortcut.pack(pady=5)
restart_shortcut_entry = tk.Entry(frame_restart_shortcut, textvariable=restart_shortcut_var, width=15)
restart_shortcut_entry.pack(side="left", padx=10)
set_restart_key_button = tk.Button(frame_restart_shortcut, text="Set Key", command=save_shortcuts, bg="#ff9800", fg="white")
set_restart_key_button.pack(side="left")

button_sfc = tk.Button(tools_frame, text="SFC - Scan and Repair", command=run_sfc, bg="#2196f3", fg="white", width=30)
button_sfc.pack(pady=5)

button_defrag = tk.Button(tools_frame, text="Defrag - Defragment Disk", command=defrag_disk, bg="#2196f3", fg="white", width=30)
button_defrag.pack(pady=5)

button_msconfig = tk.Button(tools_frame, text="MSConfig - Configure Startup", command=open_msconfig, bg="#2196f3", fg="white", width=30)
button_msconfig.pack(pady=5)

button_nslookup = tk.Button(tools_frame, text="NSLookup - Resolve Domain", command=nslookup, bg="#2196f3", fg="white", width=30)
button_nslookup.pack(pady=5)

button_ver = tk.Button(tools_frame, text="Ver - Windows Version", command=show_version, bg="#2196f3", fg="white", width=30)
button_ver.pack(pady=5)

# Button for cleaning temporary files
button_clean_temp = tk.Button(tools_frame, text="Clean Temporary Files", command=clean_temp_files, bg="#2196f3", fg="white", width=30)
button_clean_temp.pack(pady=5)

# --- Browser Manager Panel ---
browser_frame = tk.LabelFrame(root, text="Browser Management", bg="#e0e0e0", padx=10, pady=10)
browser_frame.pack(pady=10, fill="both", side="left", expand=True)

instructions_label_browsers = tk.Label(browser_frame, text="Select the browser to install or uninstall:", bg="#e0e0e0")
instructions_label_browsers.pack(pady=10)

# Create frames for each browser
browser_controls = []

def create_browser_frame(browser_name, install_command, uninstall_command):
    frame = tk.Frame(browser_frame, bg="#e0e0e0")
    frame.pack(pady=5)

    btn_install = tk.Button(frame, text=f"Install {browser_name}", command=lambda: install_browser(install_command), bg="#4caf50", fg="white")
    btn_install.pack(side="left", padx=10)

    status_label = tk.Label(frame, text="✘", font=("Arial", 14), bg="#e0e0e0")  # Initial status is 'not installed'
    status_label.pack(side="left")

    btn_uninstall = tk.Button(frame, text="Uninstall", command=lambda: uninstall_browser(uninstall_command), bg="#f44336", fg="white")
    btn_uninstall.pack(side="left", padx=10)
    btn_uninstall.config(state="disabled")  # Initially disabled

    browser_controls.append((browser_name, status_label, btn_uninstall))

# Create frames for every browser available for installation
create_browser_frame("Brave", "Brave.Brave", "Brave.Brave")
create_browser_frame("Opera", "Opera.Opera", "Opera.Opera")
create_browser_frame("Google Chrome", "Google.Chrome", "Google.Chrome")
create_browser_frame("Mozilla Firefox", "Mozilla.Firefox", "Mozilla.Firefox")
create_browser_frame("Microsoft Edge", "Microsoft.Edge", "Microsoft.Edge")
create_browser_frame("Vivaldi", "Vivaldi.Vivaldi", "Vivaldi.Vivaldi")
create_browser_frame("Internet Explorer", "InternetExplorer.InternetExplorer", "InternetExplorer.InternetExplorer")

# Text to show output
output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text, bg="#f0f0f0", anchor="w", width=50)
output_label.pack(pady=10, padx=(10, 0), fill="x", side="right")

# Label for cleaning temporary files, more visible
cleanup_label = tk.Label(tools_frame, text="Temporary file cleaning accepted:", bg="#e0e0e0")
cleanup_label.pack(pady=5, padx=(10, 5))

# Load shortcuts when the program starts
load_shortcuts()
# Check the initial status of the browsers
update_browser_status()

# Start the main loop
root.mainloop()