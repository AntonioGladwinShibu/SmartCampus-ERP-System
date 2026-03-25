import customtkinter as ctk
# Imports the customtkinter library for creating the graphical user interface.
from services.analytics_service import AnalyticsService
# Imports the AnalyticsService class to fetch statistical data from the database.

class AnalyticsPage(ctk.CTkFrame):
# Defines the AnalyticsPage class inheriting from CTkFrame to act as a container.
    def __init__(self, master, role="STUDENT", username=""):
    # Initializes the AnalyticsPage with a master window, user role, and username.
        super().__init__(master, fg_color="transparent")
        # Calls the parent class constructor and sets the background color to transparent.
        self.role = role
        # Stores the user's role to determine access rights within the page.
        
        self.header = ctk.CTkLabel(self, text="System Analytics", font=ctk.CTkFont(family="Roboto", size=24, weight="bold"), text_color=("#1A73E8", "#8AB4F8"))
        # Creates a header label displaying "System Analytics" with styling.
        self.header.pack(pady=(20, 20), padx=20, anchor="w")
        # Packs the header label to the top-left with padding.
        
        stats = AnalyticsService.get_summary_stats()
        # Retrieves the summary statistics from the analytics service.
        
        # Display Cards
        # Comment: Display Cards section
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        # Creates a frame to hold the individual statistic cards.
        self.cards_frame.pack(fill="both", expand=True, padx=20, pady=10)
        # Packs the cards frame to fill the available space.
        self.cards_frame.grid_columnconfigure((0, 1), weight=1)
        # Configures the grid columns within the cards frame to expand equally.
        
        def create_stat_card(parent, row, col, title, value, color):
        # Defines a helper function to create individual statistic cards.
            card = ctk.CTkFrame(parent, corner_radius=15, fg_color=color)
            # Creates a card frame with rounded corners and a specific background color.
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            # Places the card in the grid with padding and stretch.
            
            title_lbl = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=18, weight="bold"), text_color="white")
            # Creates a title label for the card.
            title_lbl.pack(pady=(20, 5))
            # Packs the title label into the card.
            
            val_lbl = ctk.CTkLabel(card, text=str(value), font=ctk.CTkFont(size=32, weight="bold"), text_color="white")
            # Creates a value label displaying the statistic's value.
            val_lbl.pack(pady=(5, 20))
            # Packs the value label into the card.
            
        create_stat_card(self.cards_frame, 0, 0, "Total Students", stats.get("students", 0), "#1E88E5")
        # Creates a card displaying the total number of students.
        create_stat_card(self.cards_frame, 0, 1, "Total Faculty", stats.get("faculty", 0), "#43A047")
        # Creates a card displaying the total number of faculty members.
        create_stat_card(self.cards_frame, 1, 0, "Active Courses", stats.get("courses", 0), "#E53935")
        # Creates a card displaying the total number of active courses.
        create_stat_card(self.cards_frame, 1, 1, "Library Books", stats.get("books", 0), "#FB8C00")
        # Creates a card displaying the total number of library books.
