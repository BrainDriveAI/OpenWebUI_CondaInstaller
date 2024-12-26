
import os
import shutil
import sys
import platform
import tkinter as tk
from tkinter import ttk
from card_ollama import Ollama
from card_open_webui import OpenWebUI
from card_open_webui_pipelines import OpenWebUIPipelines

from status_display import StatusDisplay
from status_updater import StatusUpdater
import threading
from AppConfig import AppConfig
from helper_image import HelperImage 
from AppDesktopIntegration import AppDesktopIntegration

def main():
    # Create the main window
    root = tk.Tk()
    root.title("BrainDrive.ai Installer [v0.3.3]")
    config = AppConfig()

    try:

        desktop_integration = AppDesktopIntegration()
        icon_path = desktop_integration.setup_application_icon()
        root.iconbitmap(icon_path)  

        def background_task():
            desktop_integration.verify_exe_exists()
            
            desktop_integration.verify_and_update_icon()

        threading.Thread(target=background_task, daemon=True).start()

    except Exception as e:
        print(f"Failed to set application icon: {e}")

 
    root.geometry("800x600")
    root.resizable(False, False)

    # Detect the OS and set the label text accordingly
    os_name = platform.system()
    if os_name == "Windows":
        version = platform.version()  # Example: '10.0.22000'
        major, minor, build = map(int, version.split('.'))
        if major == 10 and build >= 22000:
            os_text = "Using Windows 11"
        else:
            os_text = f"Using Windows {platform.release()}"
    elif os_name == "Darwin":
        os_text = "Using macOS"
    else:
        os_text = f"Using {os_name}"

    # Top section
    top_frame = tk.Frame(root, height=80, bg="lightgrey")
    top_frame.pack(fill=tk.X)

    title_label = tk.Label(top_frame, text="AI System Installer by BrainDrive.ai", font=("Arial", 24), bg="lightgrey")
    title_label.place(relx=0.5, rely=0.4, anchor="center")

    # New label for "Using Windows 10"
    os_label = tk.Label(top_frame, text=os_text, font=("Arial", 10), bg="lightgrey")
    os_label.place(relx=0.5, rely=0.8, anchor="center")

    # Create card instances
    ollama_instance = Ollama()
    webui_instance = OpenWebUI()
    pipelines_instance = OpenWebUIPipelines()

    # Middle section
    middle_frame = tk.Frame(root, height=320, width=600)
    middle_frame.pack(fill=tk.BOTH, expand=True)

    # Left group
    left_group = tk.Frame(middle_frame, width=400, height=320, relief=tk.RIDGE, bd=2)
    left_group.pack_propagate(False)
    left_group.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Right group
    right_group = tk.Frame(middle_frame, width=400, height=320, relief=tk.RIDGE, bd=2)
    right_group.pack_propagate(False)
    right_group.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


    # Bottom status section
    status_display = StatusDisplay(root)
    step_label, details_label, progress_bar = status_display.get_components()
    status_updater = StatusUpdater(step_label, details_label, progress_bar)
    config.status_display = status_display
    # Display cards with status_updater
    webui_instance.display(left_group, status_updater)
    pipelines_instance.display(right_group, status_updater)
    ollama_instance.display(right_group, status_updater)


    # Run the main loop
    root.mainloop()


if __name__ == "__main__":
    main()
