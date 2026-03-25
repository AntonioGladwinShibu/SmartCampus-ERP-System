import bcrypt
# Imports the bcrypt library for hashing passwords securely.
from config.database import db
# Imports the database instance corresponding to MongoDB.

class AuthService:
# Defines the AuthService class to encapsulate authentication-related logic.
    """Handles authentication and user management"""
    # Docstring describing the purpose of the class.
    
    @staticmethod
    # Declares the method below as static.
    def hash_password(password):
    # Defines a function to encrypt plain-text passwords.
        salt = bcrypt.gensalt()
        # Generates a random cryptographic salt using bcrypt.
        return bcrypt.hashpw(password.encode('utf-8'), salt)
        # Encodes the password as bytes, hashes it with the salt, and returns the result.
        
    @staticmethod
    # Declares the method below as static.
    def verify_password(password, hashed):
    # Defines a function to check if a plain-text password matches a previously hashed one.
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
        # Encodes the input password and uses bcrypt to verify it against the hashed DB password.
        
    @staticmethod
    # Declares the method below as static.
    def register_user(username, email, phone, password, role="STUDENT"):
    # Defines a method to create a new user account with a default role of "STUDENT".
        """Registers a new user. Default role is STUDENT."""
        # Docstring explaining what the method does.
        try:
        # Begins a try block for error handling.
            if db.users.find_one({"$or": [{"username": username}, {"email": email}, {"phone": phone}]}):
            # Checks the database to see if a user with the same username, email, or phone already exists.
                return {"success": False, "message": "User with these details already exists."}
                # Returns an error dictionary to the caller if duplicates are found.
                
            hashed_pw = AuthService.hash_password(password)
            # Hashes the plain-text password before storing it.
            user_doc = {
            # Starts defining a dictionary to represent the new user document in MongoDB.
                "username": username,
                # Assigns the username to the document.
                "email": email,
                # Assigns the email.
                "phone": phone,
                # Assigns the phone number.
                "password": hashed_pw,
                # Assigns the securely hashed password.
                "role": role.upper()
                # Ensures the role is safely converted to uppercase before saving.
            }
            # Closes the user_doc dictionary.
            db.users.insert_one(user_doc)
            # Inserts the new user document into the 'users' collection.
            return {"success": True, "message": "User registered successfully."}
            # Returns a success flag and message.
        except Exception as e:
        # Catches any unexpected errors.
            return {"success": False, "message": f"Database error: {str(e)}"}
            # Returns an error indicating a database crash or failure.

    @staticmethod
    # Declares a static method.
    def login(identifier, password):
    # Defines a login method allowing the user to sign in by identifier (username, email, or phone).
        """Login using username, email, or phone"""
        # Docstring mentioning the supported login identifiers.
        try:
        # Enters a try block.
            user = db.users.find_one({
            # Queries the 'users' collection to find a matching document.
                "$or": [
                # Specifies that any of the following conditions matching is acceptable.
                    {"username": identifier},
                    # Checks if the username matches the given identifier.
                    {"email": identifier},
                    # Checks if the email matches.
                    {"phone": identifier}
                    # Checks if the phone number matches.
                ]
                # Closes the $or condition array.
            })
            # Closes the query dictionary.
            
            if user and AuthService.verify_password(password, user.get("password")):
            # Verifies that the user exists and the provided password matches the hashed password in DB.
                return {
                # Starts building the return data structure for a successful login.
                    "success": True,
                    # Indicates the login worked.
                    "role": user.get("role", "STUDENT"), 
                    # Passes back the role of the user (or 'STUDENT' as a fallback).
                    "username": user.get("username")
                    # Retrieves and passes back the user's username.
                }
                # Finishes building the success return dictionary.
            return {"success": False, "message": "Invalid credentials."}
            # Returns a mismatch error if the user wasn't found or the password was incorrect.
        except Exception as e:
        # Catches errors like disrupted connections.
            return {"success": False, "message": f"Database error: {str(e)}"}
            # Return details about the caught database exception.