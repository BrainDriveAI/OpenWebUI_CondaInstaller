class ButtonStateManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(ButtonStateManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        if not hasattr(self, "buttons"):  # Prevent reinitialization
            self.buttons = {}

    def register_button(self, name, button):
        """
        Registers a button with a unique name.
        :param name: The unique name for the button.
        :param button: The Tkinter button instance.
        """
        self.buttons[name] = button

    def set_button_state(self, names, state):
        """
        Sets the state of one or more buttons.
        :param names: List of button names or a single name as a string.
        :param state: The desired state (e.g., "normal", "disabled").
        """
        if isinstance(names, str):
            names = [names]
        for name in names:
            if name in self.buttons:
                self.buttons[name].config(state=state)

    def disable_buttons(self, names):
        """
        Disables one or more buttons.
        """
        self.set_button_state(names, "disabled")

    def enable_buttons(self, names):
        """
        Enables one or more buttons.
        """
        self.set_button_state(names, "normal")
    
    def toggle_button_text(self, name, text1, text2):
        """
        Toggles the button text between two states.
        :param name: The unique name of the button.
        :param text1: The first text state.
        :param text2: The second text state.
        """
        if name in self.buttons:
            current_text = self.buttons[name].cget("text")
            new_text = text2 if current_text == text1 else text1
            self.buttons[name].config(text=new_text)

    def get_button_text(self, name):
        """
        Retrieves the current text of a button.
        :param name: The unique name of the button.
        :return: The text of the button, or None if the button is not registered.
        """
        if name in self.buttons:
            return self.buttons[name].cget("text")
        return None
    
    def set_button_text(self, name, new_text):
        """
        Sets the button text to the specified value.
        :param name: The unique name of the button.
        :param new_text: The new text to set for the button.
        """
        if name in self.buttons:
            self.buttons[name].config(text=new_text)
