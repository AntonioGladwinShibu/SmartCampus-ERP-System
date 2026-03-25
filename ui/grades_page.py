import customtkinter as ctk
# Imports the customtkinter library to build the graphical user interface.
from services.grade_service import GradeService
# Imports the GradeService class to handle logic related to fetching, publishing, and deleting grades.
from ui.components import ScrollableTable, display_error, display_success, create_button, create_entry
# Imports reusable UI components and helper functions for tables, messages, buttons, and input fields.

class GradesPage(ctk.CTkFrame):
# Defines the GradesPage class, which inherits from ctk.CTkFrame to act as a container frame for the page.
    def __init__(self, master, role="STUDENT", username=""):
    # Constructor method that initializes the UI frame, taking the parent widget, user's role, and username as arguments.
        super().__init__(master, fg_color="transparent")
        # Calls the parent class constructor to initialize the frame with a transparent background.
        self.role = role
        # Saves the provided user role to an instance variable.
        self.username = username
        # Saves the provided username to an instance variable.
        
        self.header = ctk.CTkLabel(self, text="Grades Management", font=ctk.CTkFont(family="Roboto", size=24, weight="bold"), text_color=("#1A73E8", "#8AB4F8"))
        # Creates a heading label for the page with specific text, font styling, and light/dark theme text colors.
        self.header.pack(pady=(20, 10), padx=20, anchor="w")
        # Places the header label on the screen with padding and aligns it to the left (west).
        
        self.status_label = ctk.CTkLabel(self, text="")
        # Creates an initially empty label used to display success or error status messages.
        self.status_label.pack(pady=5, padx=20, anchor="w")
        # Places the status label below the header with padding and aligns it to the left.
        
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        # Creates a container frame to hold action inputs and buttons (like publish and refresh), with a transparent background.
        self.action_frame.pack(fill="x", padx=20, pady=10)
        # Places the action frame on the screen, allowing it to fill the horizontal space.
        
        if self.role in ["ADMIN", "FACULTY"]:
        # Checks if the user has admin or faculty privileges to allow them to publish or delete grades.
            self.s_id_entry = create_entry(self.action_frame, placeholder="Username (Student)")
            # Creates an input field for the student's username inside the action frame.
            self.s_id_entry.pack(side="left", padx=5)
            # Places the student ID input field on the left side with padding.
            
            self.c_id_entry = create_entry(self.action_frame, placeholder="Course ID")
            # Creates an input field for the course ID.
            self.c_id_entry.pack(side="left", padx=5)
            # Places the course ID input field next to the previous one on the left.
            
            self.g_entry = create_entry(self.action_frame, placeholder="Grade (A, B, etc.)", width=120)
            # Creates an input field for the grade value with a specified width of 120 pixels.
            self.g_entry.pack(side="left", padx=5)
            # Places the grade input field next to the previous ones.
            
            self.publish_btn = create_button(self.action_frame, text="Publish Grade", command=self.publish_grade, width=120)
            # Creates a button labeled "Publish Grade" that triggers the 'publish_grade' method when clicked.
            self.publish_btn.pack(side="left", padx=5)
            # Places the publish button next to the input fields on the left.
            
            self.del_btn = create_button(self.action_frame, text="Delete Grade", command=self.delete_grade, width=120)
            # Creates a button labeled "Delete Grade" that triggers the 'delete_grade' method.
            self.del_btn.configure(fg_color="#EA4335", hover_color="#D93025")
            # Configures custom background and hover colors (shades of red) for the delete button.
            self.del_btn.pack(side="left", padx=5)
            # Places the delete button next to the publish button.
            
        self.refresh_btn = create_button(self.action_frame, text="Refresh", command=self.load_data, width=100)
        # Creates a "Refresh" button available to all roles that triggers the 'load_data' method to update the table.
        self.refresh_btn.pack(side="right", padx=5)
        # Places the refresh button on the right side of the action frame.

        columns = ["Student", "Course ID", "Grade"]
        # Defines a list of column headers for the grades table.
        self.table = ScrollableTable(self, columns=columns, width=800, height=400)
        # Creates a scrollable table UI component with the specified columns and dimensions.
        self.table.pack(padx=20, pady=10, fill="both", expand=True)
        # Places the table on the screen, letting it fill available space and expand as window size changes.
        
        self.load_data()
        # Calls the 'load_data' method immediately to populate the table when the page is initialized.

    def load_data(self):
    # Defines a method to fetch grades from the database or service and populate the table.
        if self.role == "STUDENT":
        # Checks if the current user is a student.
            grades = GradeService.get_student_grades(self.username)
            # Fetches only the grades belonging to the specific student's username.
            if not grades:
            # Checks if the returned grades list is empty.
                display_error(self.status_label, "Grade not yet published.")
                # Displays an error message on the screen if no grades are found for the student.
        else:
        # Executes this block if the user is an admin or faculty member.
            from config.database import db
            # Imports the database connection locally to avoid circular imports.
            grades = list(db.grades.find({}, {"_id": 0}))
            # Fetches all grade records from the 'grades' collection, excluding the MongoDB '_id' field.
            
        formatted = [[g.get("student_id", ""), g.get("course_id", ""), g.get("grade", "")] for g in grades]
        # Formats the retrieved grade documents into a list of lists, suitable for inserting into the UI table.
        self.table.populate(formatted)
        # Passes the formatted grades list to the table component to render the data on screen.
        
    def publish_grade(self):
    # Defines a method to gather input data and save a new grade.
        s_id = self.s_id_entry.get().strip()
        # Retrieves the text from the student ID input field and removes leading/trailing spaces.
        c_id = self.c_id_entry.get().strip()
        # Retrieves the text from the course ID input field and removes leading/trailing spaces.
        grade = self.g_entry.get().strip()
        # Retrieves the text from the grade input field and removes leading/trailing spaces.
        
        if not all([s_id, c_id, grade]):
        # Validates that all three required fields are not empty.
            display_error(self.status_label, "Enter Student, Course, and Grade.")
            # Shows an error message if any field is missing input.
            return
            # Exits the method early so the grade doesn't attempt to publish with missing data.
            
        result = GradeService.publish_grade(s_id, c_id, grade)
        # Calls the 'publish_grade' method from GradeService with the collected inputs to save to the database.
        
        if result["success"]:
        # Checks if the service successfully published the grade.
            display_success(self.status_label, "Grade published.")
            # Shows a success message to the user.
            self.load_data()
            # Refreshes the table data to show the newly published grade.
            self.s_id_entry.delete(0, "end")
            # Clears the student ID input field from the start index (0) to the end.
            self.c_id_entry.delete(0, "end")
            # Clears the course ID input field.
            self.g_entry.delete(0, "end")
            # Clears the grade input field.
        else:
        # Executes this block if publishing the grade failed.
            display_error(self.status_label, result["message"])
            # Displays the specific error message returned by the service.

    def delete_grade(self):
    # Defines a method to prompt the user and delete a specific grade entry.
        dialog = ctk.CTkInputDialog(text="Enter format 'student_id,course_id' to delete:", title="Delete Grade")
        # Opens a popup input dialog asking the user to enter the target student and course IDs separated by a comma.
        inp = dialog.get_input()
        # Retrieves the text input provided by the user in the dialog box.
        if inp and "," in inp:
        # Checks if the user provided input and if that input contains a comma separator.
            s_id, c_id = inp.split(",", 1)
            # Splits the input string at the first comma into two variables: student ID and course ID.
            from config.database import db
            # Imports the database connection locally.
            res = db.grades.delete_one({"student_id": s_id.strip(), "course_id": c_id.strip()})
            # Executes a database query to delete one record that matches both the student ID and course ID.
            if res.deleted_count > 0:
            # Checks if any documents were actually deleted by the database operation.
                display_success(self.status_label, "Grade deleted successfully.")
                # Displays a success message indicating the grade was removed.
                self.load_data()
                # Refreshes the table data to reflect the deleted grade.
            else:
            # Executes this block if no matching document was found to delete.
                display_error(self.status_label, "Grade not found.")
                # Displays an error message informing the user that the specified grade does not exist.