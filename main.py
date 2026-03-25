import customtkinter as ctk
# Imports the customtkinter library for building the main application window.
from config.database import db  # Ensures DB connects on startup
# Imports the database instance, which triggers the connection to MongoDB when the app starts.
from ui.login import LoginPage
# Imports the LoginPage class to display it as the first screen.

class App(ctk.CTk):
# Defines the main App class, inheriting from ctk.CTk, representing the main window.
    def __init__(self):
    # Constructor method for the App class to initialize the window.
        super().__init__()
        # Calls the parent constructor to initialize the customtkinter window.

        self.title("SCMS - College Management System")
        # Sets the title of the main application window.
        self.geometry("1000x700")
        # Sets the initial size of the window to 1000 pixels wide by 700 pixels tall.
        self.minsize(800, 600)
        # Sets the minimum allowed size for the window to prevent the UI from squishing.
        
        # Configure grid for the container frame
        # Comment: Configure grid for the container frame
        self.grid_rowconfigure(0, weight=1)
        # Configures the first row of the grid layout to expand and fill available vertical space.
        self.grid_columnconfigure(0, weight=1)
        # Configures the first column of the grid layout to expand and fill available horizontal space.
        
        self.current_frame = None
        # Initializes a variable to keep track of the currently displayed frame/page.
        
        # Show login page on startup
        # Comment: Show login page on startup
        self.show_frame(LoginPage)
        # Calls the show_frame method to display the LoginPage when the app launches.

    def show_frame(self, frame_class, **kwargs):
    # Defines a method to switch between different frames/pages in the application.
        """Destroys current frame and shows the requested one"""
        # Docstring explaining that the method destroys the old frame and renders the new one.
        if self.current_frame is not None:
        # Checks if there is already a frame being displayed on the screen.
            self.current_frame.destroy()
            # Destroys the current frame to clear the screen and free up memory.
            
        self.current_frame = frame_class(self, **kwargs)
        # Instantiates the new frame class, passing 'self' (the app window) as the master, along with any extra arguments.
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        # Places the new frame in the grid, spanning all directions (north, south, east, west) to fill the window.


if __name__ == "__main__":
# Checks if the script is being run directly (not imported as a module).
    # Setup visual appearance
    # Comment: Setup visual appearance
    ctk.set_appearance_mode("Dark")
    # Sets the global appearance mode of customtkinter to "Dark" theme.
    ctk.set_default_color_theme("blue")
    # Sets the default color theme for widgets (buttons, etc.) to "blue".
    
    app = App()
    # Creates an instance of the App class, initializing the main window.
    app.mainloop()
    # Starts the Tkinter event loop to keep the application running and responsive.