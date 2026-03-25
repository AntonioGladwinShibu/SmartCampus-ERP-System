import customtkinter as ctk
# Imports the customtkinter library for the user interface components.
from services.attendance_service import AttendanceService
# Imports the AttendanceService class to interact with attendance data.
from ui.components import ScrollableTable, display_error, display_success, create_button, create_entry
# Imports custom UI components like tables, buttons, entries, and message displays.
from datetime import date
# Imports the date object from datetime to get the current date for attendance marking.

class AttendancePage(ctk.CTkFrame):
# Defines the AttendancePage class inheriting from CTkFrame.
    def __init__(self, master, role="STUDENT", username=""):
    # Initializes the page with master framework, user role, and identifying username.
        super().__init__(master, fg_color="transparent")
        # Calls the parent constructor setting a transparent background color.
        self.role = role
        # Saves the user's role to determine available controls.
        self.username = username
        # Saves the username to fetch specific student data if needed.
        
        self.header = ctk.CTkLabel(self, text="Attendance Management", font=ctk.CTkFont(family="Roboto", size=24, weight="bold"), text_color=("#1A73E8", "#8AB4F8"))
        # Creates the main header label for the page.
        self.header.pack(pady=(20, 10), padx=20, anchor="w")
        # Packs the header to the top left of the frame.
        
        self.status_label = ctk.CTkLabel(self, text="")
        # Creates a label to display error or success messages to the user.
        self.status_label.pack(pady=5, padx=20, anchor="w")
        # Packs the status label beneath the header.
        
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        # Creates a frame to hold action controls like inputs and buttons.
        self.action_frame.pack(fill="x", padx=20, pady=10)
        # Packs the action frame horizontally spanning the width.
        
        if self.role in ["ADMIN", "FACULTY"]:
        # Checks if the current user has administrative or faculty privileges.
            self.s_id_entry = create_entry(self.action_frame, placeholder="Username (Student)")
            # Creates an entry field for inputting the student's username.
            self.s_id_entry.pack(side="left", padx=5)
            # Packs the student ID entry to the left side of the action frame.
            
            self.c_id_entry = create_entry(self.action_frame, placeholder="Course ID")
            # Creates an entry field for inputting the course ID.
            self.c_id_entry.pack(side="left", padx=5)
            # Packs the course ID entry next to the student entry.
            
            self.status_var = ctk.StringVar(value="Present")
            # Initializes a string variable for the dropdown, defaulting to "Present".
            self.status_opt = ctk.CTkOptionMenu(
            # Creates an option menu dropdown to select attendance status.
                self.action_frame, 
                # Sets the parent frame.
                values=["Present", "Absent", "Late"],
                # Defines the available options in the dropdown.
                variable=self.status_var,
                # Links the dropdown selection to the status_var variable.
                width=100
                # Sets the width of the dropdown menu.
            )
            # Closes the CTkOptionMenu initialization.
            self.status_opt.pack(side="left", padx=5)
            # Packs the dropdown menu to the left.
            
            self.mark_btn = create_button(self.action_frame, text="Mark", command=self.mark_attendance, width=80)
            # Creates a button to submit the attendance mark.
            self.mark_btn.pack(side="left", padx=5)
            # Packs the mark button into the frame.
            
            self.del_btn = create_button(self.action_frame, text="Delete", command=self.delete_attendance, width=80)
            # Creates a delete button to remove an attendance record.
            self.del_btn.configure(fg_color="#EA4335", hover_color="#D93025")
            # Configures the delete button with a red color scheme.
            self.del_btn.pack(side="left", padx=5)
            # Packs the delete button into the frame.
            
        self.refresh_btn = create_button(self.action_frame, text="Refresh", command=self.load_data, width=100)
        # Creates a refresh button to manually reload table data.
        self.refresh_btn.pack(side="right", padx=5)
        # Packs the refresh button to the right side of the action frame.

        columns = ["Student", "Course ID", "Date", "Status"]
        # Defines the column headers for the data table.
        self.table = ScrollableTable(self, columns=columns, width=800, height=400)
        # Creates an instance of the custom ScrollableTable component.
        self.table.pack(padx=20, pady=10, fill="both", expand=True)
        # Packs the table to fill the remaining space in the frame.
        
        self.load_data()
        # Initial call to populate the table with data upon page creation.

    def load_data(self):
    # Defines the method to load attendance data into the table.
        if self.role == "STUDENT":
        # Checks if the user is a student to filter data.
            att = AttendanceService.get_student_attendance(self.username)
            # Fetches attendance records only for the logged-in student.
        else:
        # Executes if the user is an Admin or Faculty.
            from config.database import db
            # Imports the database instance directly.
            att = list(db.attendance.find({}, {"_id": 0}))
            # Fetches all attendance records from the database collection.
            
        formatted = [[a.get("student_id", ""), a.get("course_id", ""), a.get("date", ""), a.get("status", "")] for a in att]
        # Formats the fetched dictionaries into a list of lists matching table columns.
        self.table.populate(formatted)
        # Populates the table widget with the formatted data.
        
    def mark_attendance(self):
    # Defines the method to process marking attendance.
        s_id = self.s_id_entry.get().strip()
        # Retrieves and trims the student ID string from the entry box.
        c_id = self.c_id_entry.get().strip()
        # Retrieves and trims the course ID string from the entry box.
        status = self.status_var.get()
        # Retrieves the selected status from the dropdown menu.
        today = str(date.today())
        # Converts today's local date into string format.
        
        if not all([s_id, c_id]):
        # Checks if both student ID and course ID fields are filled out.
            display_error(self.status_label, "Enter Student Username and Course ID.")
            # Displays an error message asking to complete the fields.
            return
            # Exits the function early.
            
        result = AttendanceService.mark_attendance(s_id, c_id, status, today)
        # Calls the backend service to update or insert the attendance record.
        
        if result["success"]:
        # Verifies if the service operation succeeded.
            display_success(self.status_label, "Attendance marked.")
            # Shows a green success message.
            self.load_data()
            # Reloads the table to reflect the new update.
        else:
        # Executes if the operation failed.
            display_error(self.status_label, result["message"])
            # Shows a red error message corresponding to the failure detail.

    def delete_attendance(self):
    # Defines an auxiliary method to remove specific attendance entries.
        dialog = ctk.CTkInputDialog(text="Enter format 'student_id,course_id,date' to delete:", title="Delete Attendance")
        # Spawns a modal dialog asking the admin for identification parameters.
        inp = dialog.get_input()
        # Retrieves the text submitted by the user in the prompt.
        if inp and "," in inp:
        # Confirms an input string exists and has a comma format.
            parts = [p.strip() for p in inp.split(",", 2)]
            # Splits the input by commas and removes whitespace from segments.
            if len(parts) == 3:
            # Assures exactly three matching parameters exist.
                s_id, c_id, date_str = parts
                # Unpacks the parsed segments into specific variables.
                from config.database import db
                # Re-imports the database variable locally.
                res = db.attendance.delete_one({"student_id": s_id, "course_id": c_id, "date": date_str})
                # Invokes a single document delete query based on composite keys.
                if res.deleted_count > 0:
                # Verifies if a real document was eliminated from the collection.
                    display_success(self.status_label, "Attendance deleted.")
                    # Issues a confirming response onto the alert label.
                    self.load_data()
                    # Resets the table dynamically parsing the updated dataset.
                else:
                # Triggers if the query found zero matching documents.
                    display_error(self.status_label, "Attendance record not found.")
                    # Reports failure to find targeted deletion item.
            else:
            # Catches incorrectly formatted prompt text with insufficient commas.
                display_error(self.status_label, "Invalid format.")
                # Asserts a syntax breakdown.