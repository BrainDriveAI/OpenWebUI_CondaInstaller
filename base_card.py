from abc import ABC, abstractmethod
from AppConfig import AppConfig 

class BaseCard(ABC):
    """
    Abstract base class to enforce a common structure for all card-related classes.
    """
    def __init__(self, name, description, size):
        self.name = name
        self.description = description
        self.size = size
        self.parent_frame = None
        self.config = AppConfig()

    def set_parent_frame(self, parent_frame):
        """
        Sets the parent frame where the card is displayed.
        :param parent_frame: The Tkinter frame.
        """
        self.parent_frame = parent_frame

    def refresh_display(self):
        """
        Refreshes the card UI by clearing and re-displaying it.
        Subclasses should override this method for specific UI logic.
        """
        if self.parent_frame:
            for widget in self.parent_frame.winfo_children():
                widget.destroy()  # Clear existing widgets
            self.display(self.parent_frame)  # Re-display the card
        else:
            print(f"No parent frame set for {self.name}. Cannot refresh display.")



    @abstractmethod
    def install(self):
        """
        Method to handle installation logic. Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def uninstall(self):
        """
        Method to handle uninstallation logic. Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def get_status(self):
        """
        Method to retrieve the status of the card's functionality.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def display(self, parent_frame):
        """
        Displays the card UI within the given Tkinter frame.
        """
        pass