from base_card import BaseCard
import tkinter as tk
from PIL import Image, ImageTk

class OpenWebUIPipelines(BaseCard):
    def __init__(self):
        super().__init__(name="Open WebUI Pipelines", description="Pipelines are designed to automate the execution of tasks by linking multiple processes together in a seamless manner.", 
        size="2.0GB")
        self.installed = False

    def install(self):
        """
        Implements the installation logic for Open WebUI Pipelines.
        """
        print(f"Installing {self.name}...")
        import time
        time.sleep(3)  # Simulate installation time
        self.installed = True
        print(f"{self.name} installation complete.")

    def uninstall(self):
        """
        Implements the uninstallation logic for Open WebUI Pipelines.
        """
        if self.installed:
            print(f"Uninstalling {self.name}...")
            import time
            time.sleep(2)  # Simulate uninstallation time
            self.installed = False
            print(f"{self.name} uninstallation complete.")
        else:
            print(f"{self.name} is not installed.")

    def get_status(self):
        """
        Returns the installation status of Open WebUI Pipelines.
        """
        return f"{self.name} is {'installed' if self.installed else 'not installed'}."

    def display(self, parent_frame, status_updater):
        """
        Displays the card UI within the given Tkinter frame.
        """

        self.set_parent_frame(parent_frame)
        card_frame = tk.Frame(parent_frame, relief=tk.GROOVE, bd=2)
        card_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        card_image = Image.open("testicon.png")
        card_image.thumbnail((50, 50))
        card_photo = ImageTk.PhotoImage(card_image)

        ollama_icon = tk.Label(card_frame, image=card_photo)
        ollama_icon.image = card_photo  # Keep a reference
        ollama_icon.place(x=10, y=10)

        card_label = tk.Label(card_frame, text=self.name, font=("Arial", 16))
        card_label.place(relx=0.5, y=20, anchor="center")

        card_info = tk.Label(
            card_frame,
            text=self.description,
            font=("Arial", 10),
            wraplength=350,
            justify="left"
        )
        card_info.place(x=10, y=70)

        size_label = tk.Label(card_frame, text=f"Size: {self.size}", font=("Arial", 9))
        size_label.place(x=10, rely=1.0, anchor="sw", y=-10)


        auto_button = tk.Button(card_frame, text="Auto", state=tk.DISABLED)
        auto_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

        install_button = tk.Button(card_frame, text="Install", command=self.install)
        # install_button.place(relx=1.0, rely=1.0, anchor="se", x=-90, y=-10)

        uninstall_button = tk.Button(card_frame, text="Uninstall", command=self.uninstall)
        # uninstall_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

        status_button = tk.Button(
            card_frame,
            text="Status",
            command=lambda: print(self.get_status())
        )
        # status_button.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)