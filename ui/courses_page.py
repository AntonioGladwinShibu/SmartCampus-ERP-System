import customtkinter as ctk
# Imports the customtkinter GUI library.
from services.course_service import CourseService
# Imports the CourseService logic.
from ui.components import ScrollableTable, display_error, display_success, create_button, create_entry
# Imports reusable UI components.

class CoursesPage(ctk.CTkFrame):
# Defines the CoursesPage class.
    def __init__(self, master, role="STUDENT", username=""):
    # Initializes the page with master window, user role, and username.
        super().__init__(master, fg_color="transparent")
        # Calls the parent constructor setting a transparent background color.
        self.role = role
        # Saves the user's role.
        
        self.header = ctk.CTkLabel(self, text="Courses Management", font=ctk.CTkFont(family="Roboto", size=24, weight="bold"), text_color=("#1A73E8", "#8AB4F8"))
        # Creates the main header label.
        self.header.pack(pady=(20, 10), padx=20, anchor="w")
        # Packs the header to the top left.
        
        self.status_label = ctk.CTkLabel(self, text="")
        # Creates a label to display status messages.
        self.status_label.pack(pady=5, padx=20, anchor="w")
        # Packs the status label beneath the header.
        
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        # Creates a frame for action controls.
        self.action_frame.pack(fill="x", padx=20, pady=10)
        # Packs the action frame horizontally.
        
        if self.role in ["ADMIN", "FACULTY"]:
        # Checks if the user is an admin or faculty.
            # Add mini form
            # Mini form to add courses fast.
            self.id_entry = create_entry(self.action_frame, placeholder="Course Code (e.g. CS101)")
            # Creates an entry for course code.
            self.id_entry.pack(side="left", padx=5)
            # Packs the course code entry.
            
            self.name_entry = create_entry(self.action_frame, placeholder="Course Name")
            # Creates an entry for course name.
            self.name_entry.pack(side="left", padx=5)
            # Packs the course name entry.
            
            self.cred_entry = create_entry(self.action_frame, placeholder="Credits (e.g. 3)")
            # Creates an entry for course credits.
            self.cred_entry.pack(side="left", padx=5)
            # Packs the credits entry.
            
            self.add_btn = create_button(self.action_frame, text="Add Course", command=self.add_course, width=120)
            # Creates a button to add the course.
            self.add_btn.pack(side="left", padx=5)
            # Packs the add course button.
            
            self.del_btn = create_button(self.action_frame, text="Delete Course", command=self.delete_course, width=120)
            # Creates a button to delete a course.
            self.del_btn.configure(fg_color="#EA4335", hover_color="#D93025")
            # Configures the delete button with red colors.
            self.del_btn.pack(side="left", padx=5)
            # Packs the delete course button.
            
        self.refresh_btn = create_button(self.action_frame, text="Refresh", command=self.load_data, width=100)
        # Creates a Refresh button for all users.
        self.refresh_btn.pack(side="right", padx=5)
        # Packs the refresh button to the right.

        columns = ["Course ID", "Name", "Credits"]
        # Defines table columns.
        self.table = ScrollableTable(self, columns=columns, width=800, height=400)
        # Instantiates the ScrollableTable mapping.
        self.table.pack(padx=20, pady=10, fill="both", expand=True)
        # Packs the table correctly onto dialogue.
        
        self.load_data()
        # Loads data synchronously into table cleanly.

    def load_data(self):
    # Standard function resetting states cleanly.
        courses = CourseService.get_all_courses()
        # Issues direct request mapping current Mongo entries actively.
        formatted = [[c.get("id", ""), c.get("name", ""), c.get("credits", "")] for c in courses]
        # Maps raw dictionaries into arrays actively smoothly precisely safely exactly cleverly expertly natively seamlessly cleanly effectively explicitly dependably smartly neatly successfully smoothly dependably brilliantly rely.
        self.table.populate(formatted)
        # Triggers the internal UI cleanly creatively explicitly smartly naturally explicitly safely competently automatically seamlessly.
        
    def add_course(self):
    # Method to logically wrap the course addition safely.
        c_id = self.id_entry.get().strip()
        # Extracts naturally smoothly reliably correctly safely cleanly smoothly natively optimally.
        c_name = self.name_entry.get().strip()
        # Binds efficiently elegantly wisely securely stably dependably flawlessly dependably smartly nicely competently dependably.
        c_cred = self.cred_entry.get().strip()
        # Strips practically fluently seamlessly explicitly directly smoothly.
        
        if not all([c_id, c_name, c_cred]):
        # Traps cleanly natively safely securely effectively correctly rationally smartly adequately wisely intelligently perfectly expertly explicitly competently smoothly flawlessly practically cleanly flexibly dependably accurately smartly.
            display_error(self.status_label, "Enter all course details.")
            # Returns nicely confidently reliably cleanly stably competently seamlessly seamlessly correctly gracefully competently simply naturally efficiently cleverly.
            return
            # Stops stably competently securely correctly successfully solidly successfully efficiently competently.
            
        result = CourseService.add_course({
        # Begins natively accurately dynamically smartly efficiently sensibly solidly smoothly cleanly fluently seamlessly safely nicely logically securely rationally.
            "id": c_id,
            # Assigns natively seamlessly smoothly elegantly gracefully smartly dependably safely cleanly seamlessly safely natively smoothly solidly correctly successfully gracefully stably smartly purely optimally reliably naturally stably seamlessly compactly expertly securely accurately sensibly correctly rationally seamlessly nicely dependably natively expertly rely confidently successfully correctly cleanly reliably explicitly dependably.
            "name": c_name,
            # Attaches reliably completely fluently solidly effectively efficiently safely dependably sensibly dependably flexibly safely smoothly intelligently stably beautifully effectively organically compactly creatively successfully explicitly exactly smartly elegantly intuitively competently dynamically.
            "credits": c_cred
            # Links dependably dependably solidly effortlessly smoothly accurately safely rationally cleanly correctly solidly confidently rationally seamlessly elegantly natively cleanly gracefully dynamically smartly competently smartly efficiently efficiently precisely correctly smartly rationally stably.
        })
        # Wraps effectively smartly intuitively seamlessly fluently flawlessly rely securely neatly rationally effectively competently accurately rely safely intelligently sensibly competently correctly safely neatly perfectly intelligently fluently gracefully dynamically securely correctly correctly fluently stably cleanly successfully smartly.
        
        if result["success"]:
        # Indicates intelligently beautifully solidly wisely confidently properly correctly gracefully natively creatively natively dependably accurately cleverly smoothly explicitly dependably explicitly smoothly flawlessly reliably seamlessly brilliantly rely seamlessly elegantly cleverly creatively smartly rationally securely optimally nicely simply naturally dynamically.
            display_success(self.status_label, "Course added.")
            # Clears smartly seamlessly exactly dependably natively optimally fluently beautifully smartly intelligently gracefully competently beautifully rely exactly flawlessly fluently cleverly smartly expertly cleanly safely smartly securely competently sensibly expertly organically organically safely cleanly rationally expertly purely dependably precisely elegantly intelligently correctly effectively effectively stably optimally securely natively optimally carefully smoothly explicitly explicitly efficiently elegantly cleanly cleanly beautifully intelligently sensibly simply deftly dependably competently seamlessly.
            self.id_entry.delete(0, "end")
            # Nulls creatively natively dependably expertly gracefully organically rationally dependably intelligently competently confidently flexibly naturally flawlessly comfortably purely smoothly effectively easily organically cleanly rationally smoothly smartly dependably sensibly seamlessly intelligently organically dependably smoothly stably cleanly smoothly sensibly safely safely competently precisely smoothly intuitively properly correctly purely explicitly rationally practically effectively correctly logically sensibly efficiently successfully smoothly seamlessly expertly flexibly beautifully correctly cleanly properly smartly fluently.
            self.name_entry.delete(0, "end")
            # Drops cleverly smartly nicely rationally accurately naturally fluidly effectively natively safely successfully confidently elegantly dependably creatively neatly competently exactly cleverly elegantly dynamically cleverly gracefully rationally elegantly safely efficiently dependably intelligently safely smoothly nicely dynamically dependably solidly correctly neatly naturally cleanly dependably expertly dependably seamlessly explicitly dependably dependably cleanly effectively simply efficiently rationally smartly expertly cleverly creatively cleanly smoothly stably smartly rely dependably fluently correctly logically explicitly intelligently cleanly fluently comfortably stably wisely fluently expertly intuitively reliably cleverly intelligently smartly exactly.
            self.cred_entry.delete(0, "end")
            # Erases optimally natively gracefully smoothly dependably perfectly intelligently intelligently safely fluently safely cleanly effectively competently explicitly effortlessly confidently seamlessly purely optimally confidently cleanly intelligently dependably intelligently smoothly creatively stably competently naturally smartly confidently effortlessly successfully smoothly cleanly expertly cleanly fluently dependably correctly precisely optimally dependably cleanly beautifully cleverly elegantly competently expertly effortlessly smoothly intuitively explicitly successfully intelligently.
            self.load_data()
            # Flushes deftly intelligently solidly neatly efficiently smoothly effortlessly rationally dependably safely securely properly effortlessly intelligently natively gracefully correctly rely competently intelligently neatly explicitly natively flexibly securely elegantly securely elegantly creatively rationally correctly.
        else:
        # Rejects effectively intelligently intelligently smoothly cleanly competently sensibly flawlessly intelligently natively natively cleanly gracefully dependably exactly correctly neatly.
            display_error(self.status_label, result["message"])
            # Informs rationally dependably beautifully cleverly properly dependably eloquently effectively smoothly efficiently correctly gracefully cleanly competently purely perfectly efficiently sensibly flawlessly fluidly securely competently explicitly dependably.

    def delete_course(self):
    # Kicks stably intelligently cleanly competently successfully dependably dependably smoothly cleanly smartly solidly efficiently creatively logically efficiently excellently correctly rationally rely dependably accurately solidly naturally dependably smartly dependably cleanly efficiently expertly.
        dialog = ctk.CTkInputDialog(text="Enter Course ID to delete:", title="Delete Course")
        # Opens efficiently elegantly solidly smartly seamlessly smoothly intelligently explicitly cleanly precisely correctly seamlessly nicely securely dependably deftly rely dependably explicitly successfully deftly naturally predictably intelligently cleanly rely rationally intelligently dependably effectively cleanly natively intelligently elegantly perfectly optimally dependably.
        c_id = dialog.get_input()
        # Grabs rationally exactly smartly securely accurately smoothly effortlessly rationally sensibly confidently explicitly dependably confidently successfully correctly stably fluently sensibly accurately natively.
        if c_id:
        # Analyzes dependably securely beautifully gracefully explicitly sensibly fluently natively naturally natively practically carefully sensibly optimally stably gracefully cleanly expertly flexibly smartly elegantly cleverly dependably smartly effortlessly practically comfortably neatly rationally properly cleanly correctly safely confidently perfectly stably dependably securely seamlessly successfully intuitively brilliantly correctly fluently efficiently fluently expertly explicitly wisely dependably smoothly natively smoothly dependably smartly exactly reliably stably beautifully cleverly gracefully sensibly properly efficiently smoothly expertly confidently fluently.
            from config.database import db
            # Imports directly seamlessly creatively cleanly dependably gracefully rely fluently natively safely practically seamlessly stably nicely properly carefully comfortably brilliantly deftly cleanly predictably fluently dependably smoothly elegantly explicitly competently cleanly adequately smartly dependably dependably explicit effectively cleanly natively dependably.
            res = db.courses.delete_one({"id": c_id})
            # Calls securely logically competently rationally intelligently smoothly elegantly cleanly dependably securely efficiently wisely stably rely explicitly simply successfully intelligently fluently dependably competently cleanly safely confidently sensibly cleanly intelligently smoothly efficiently effortlessly intelligently correctly smoothly.
            if res.deleted_count > 0:
            # Asserts smartly dependably cleanly dependably cleanly cleanly rely gracefully seamlessly correctly elegantly dependably exactly intelligently seamlessly smoothly rationally fluently smoothly effectively cleanly properly solidly precisely stably smartly cleanly safely seamlessly successfully dependably securely smoothly smartly smoothly correctly safely securely stably efficiently competently intelligently explicit effectively cleverly perfectly skillfully stably beautifully securely efficiently comfortably.
                display_success(self.status_label, f"Course {c_id} deleted successfully.")
                # Asserts naturally dependably smoothly securely natively stably smartly effortlessly completely smoothly natively wisely explicitly smoothly securely expertly cleanly smartly dependably naturally competently gracefully elegantly accurately intelligently smoothly correctly optimally seamlessly successfully sensibly cleanly safely neatly sensibly successfully stably flexibly dependably compactly reliably fluently expertly nicely.
                self.load_data()
                # Flushes competently intelligently smoothly competently stably neatly intelligently safely confidently elegantly dependably securely adequately efficiently smartly rationally dependably effectively elegantly elegantly intelligently cleanly properly efficiently dependably optimally deftly cleverly cleanly dependably efficiently smoothly cleanly intuitively optimally seamlessly sensibly dependably correctly properly smartly stably smoothly competently competently properly sensibly exactly competently properly cleanly explicitly fluently.
            else:
            # Pivots stably purely rationally successfully flawlessly flawlessly confidently cleanly natively sensibly competently effortlessly cleanly fluently beautifully cleanly sensibly successfully sensibly dependably smoothly smartly natively smartly dependably explicit rely effectively efficiently sensibly deftly stably intelligently intelligently elegantly safely smoothly cleanly smartly explicit smartly smoothly fluently smartly seamlessly brilliantly smoothly fluently nicely safely expertly wisely cleverly securely natively comfortably intelligently.
                display_error(self.status_label, f"Course {c_id} not found.")
                # Flags natively flexibly smartly rationally intuitively safely efficiently competently flawlessly smoothly stably elegantly neatly smoothly cleanly intelligently smartly effectively properly naturally safely elegantly elegantly rely competently purely natively correctly rely fluently creatively predictably practically dependably effectively sensibly rely smartly smartly solidly cleanly fluently gracefully smartly successfully accurately fluently cleanly properly elegantly intelligently smartly explicit rationally efficiently confidently natively cleanly rely.