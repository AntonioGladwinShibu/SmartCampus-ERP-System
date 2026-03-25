from config.database import db
# Imports the active database client from the config module.
from utils.validators import capitalize_data
# Imports a utility function designed to standardize and uppercase specific core fields.

class CourseService:
# Defines the CourseService class handling course addition, retrieval, update, and deletion.
    @staticmethod
    # Declares the subsequent method statically.
    def add_course(data):
    # Method to insert a new course document into the database using a dictionary of data.
        try:
        # Opens an error handling block.
            data = capitalize_data(data)
            # Passes incoming data through the validator to uppercase specific fields.
            db.courses.insert_one(data)
            # Inserts the cleanly formatted document into the courses collection.
            return {"success": True, "message": "Course added successfully."}
            # Provides a successful feedback dictionary.
        except Exception as e:
        # Catches issues like connection drops.
            return {"success": False, "message": str(e)}
            # Emits the exception string directly.

    @staticmethod
    # Function tag.
    def update_course(course_id, data):
    # Method designed to patch properties on an existing course based on ID string.
        try:
        # Safe run wrapper.
            data = capitalize_data(data)
            # Normalizes data formats matching insert conventions.
            db.courses.update_one({"id": course_id}, {"$set": data})
            # Locates standard ID parameter and overwrites only the keys dictated in $set data payload.
            return {"success": True, "message": "Course updated successfully."}
            # Relays success notice to UI/caller.
        except Exception as e:
        # Catch errors.
            return {"success": False, "message": str(e)}
            # Fallback error messaging.

    @staticmethod
    # Makes this method invokable without instantiation.
    def delete_course(course_id):
    # Method isolating and removing an explicit course entity.
        try:
        # Protected block.
            db.courses.delete_one({"id": course_id})
            # Searches courses collection where internal string 'id' matches parameter and deletes.
            return {"success": True, "message": "Course deleted successfully."}
            # Triggers success dialogue.
        except Exception as e:
        # Fault isolation.
            return {"success": False, "message": str(e)}
            # Reports glitch.

    @staticmethod
    # Method scope modifier.
    def get_all_courses():
    # Method to retrieve total active courses list.
        try:
        # Error barrier.
            return list(db.courses.find({}, {"_id": 0}))
            # Queries MongoDB for everything, stripping the ObjectID wrapper prior to formatting to standard list.
        except Exception:
        # Catches broken queries.
            return []
            # Returns an empty list so loops elsewhere don't panic on NoneTypes.