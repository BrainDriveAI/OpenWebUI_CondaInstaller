
import os
import shutil
import sys
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


def main():
    # Create the main window
    root = tk.Tk()
    root.title("Open WebUI Installer [v0.2.3]")
    config = AppConfig()

    try:
        # Base paths
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        icon_source_path = os.path.join(base_path, 'DigitalBrainBaseIcon.ico')
        icon_dest_path = os.path.join(config.base_path, 'DigitalBrainBaseIcon.ico')
        
        if not os.path.exists(icon_dest_path):
            if os.path.exists(icon_source_path):
                shutil.copy2(icon_source_path, icon_dest_path)
            else:
                raise FileNotFoundError(f"Icon file not found at {icon_source_path}")
        root.iconbitmap(icon_dest_path)
    except Exception as e:
        print(f"Failed to set application icon: {e}")

 
    root.geometry("800x600")
    root.resizable(False, False)

    # Top section
    top_frame = tk.Frame(root, height=80, bg="lightgrey")
    top_frame.pack(fill=tk.X)

    title_label = tk.Label(top_frame, text="AI System Installer by BrainDrive.ai", font=("Arial", 24), bg="lightgrey")
    title_label.place(relx=0.5, rely=0.5, anchor="center")

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
