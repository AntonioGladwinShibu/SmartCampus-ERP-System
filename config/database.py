import pymongo
# Imports the pymongo library to interact with the MongoDB database.
from pymongo.errors import ConnectionFailure
# Imports the ConnectionFailure exception to handle database connection errors.
import sys
# Imports the sys module to allow exiting the program on critical errors.

class Database:
# Defines the Database class to manage the MongoDB connection.
    _instance = None
    # Initializes a class-level variable to implement the Singleton design pattern.

    def __new__(cls):
    # Overrides the __new__ method to control object creation for the Singleton pattern.
        if cls._instance is None:
        # Checks if an instance of the Database class already exists.
            cls._instance = super(Database, cls).__new__(cls)
            # Creates a new instance if one does not exist and assigns it to the class variable.
            cls._instance._init_db()
            # Calls the internal initialization method to set up the database connection.
        return cls._instance
        # Returns the single, shared instance of the Database class.

    def _init_db(self):
    # Defines the initialization method to connect to the database and set up collections.
        try:
        # Starts a try block to catch potential ConnectionFailure exceptions during setup.
            # Connect to local MongoDB instance
            # Comment: Connect to local MongoDB instance
            self.client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
            # Initializes the MongoDB client connecting to localhost with a 5-second timeout.
            self.client.admin.command('ping') # Test connection
            # Sends a 'ping' command to the admin database to verify the connection is active.
            self.db = self.client["scms_erp"]
            # Selects the specific database named 'scms_erp' for this application.
            
            # Setup collections
            # Comment: Setup collections
            self.users = self.db["users"]
            # Assigns the 'users' collection to an instance variable for easy access.
            self.students = self.db["students"]
            # Assigns the 'students' collection to an instance variable.
            self.faculty = self.db["faculty"]
            # Assigns the 'faculty' collection to an instance variable.
            self.courses = self.db["courses"]
            # Assigns the 'courses' collection to an instance variable.
            self.attendance = self.db["attendance"]
            # Assigns the 'attendance' collection to an instance variable.
            self.grades = self.db["grades"]
            # Assigns the 'grades' collection to an instance variable.
            self.library = self.db["library"]
            # Assigns the 'library' collection to an instance variable.
            self.fees = self.db["fees"]
            # Assigns the 'fees' collection to an instance variable.
            self.payroll = self.db["payroll"]
            # Assigns the 'payroll' collection to an instance variable.
            self.menu = self.db["menu"]
            # Assigns the 'menu' collection to an instance variable.
            self.orders = self.db["orders"]
            # Assigns the 'orders' collection to an instance variable.
            
            # Create indexes for unique constraints
            # Comment: Create indexes for unique constraints
            self.users.create_index("username", unique=True)
            # Creates a unique index on the 'username' field in the 'users' collection to prevent duplicates.
            self.users.create_index("email", unique=True)
            # Creates a unique index on the 'email' field in the 'users' collection.
            self.users.create_index("phone", unique=True)
            # Creates a unique index on the 'phone' field in the 'users' collection.
            
        except ConnectionFailure:
        # Catches the ConnectionFailure exception if MongoDB is not reachable.
            print("Failed to connect to MongoDB. Please ensure MongoDB is running on localhost:27017.")
            # Prints an error message instructing the user to check their MongoDB installation.
            sys.exit(1)
            # Exits the application entirely with an error code since the database is required.

# Singleton access point
# Comment: Singleton access point
db = Database()
# Creates or retrieves the single Database instance to be imported by other modules.