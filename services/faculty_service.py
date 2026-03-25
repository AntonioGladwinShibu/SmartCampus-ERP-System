from config.database import db
# Retrieves the initialized MongoDB database instance.
from utils.validators import capitalize_data
# Imports a helper script to enforce uppercase text formats to save cleanly.

class FacultyService:
# Sets up the main organizational class regarding teacher and faculty logic.
    @staticmethod
    # Identifies the immediate following method as static.
    def add_faculty(data):
    # Takes incoming dictionary payload to insert a staff member.
        try:
        # Envelops action in try block to avert crashes.
            data = capitalize_data(data)
            # Modifies payload, forcing targeted string fields into uppercase formats.
            db.faculty.insert_one(data)
            # Executes a write command logging the new document entirely.
            return {"success": True, "message": "Faculty added successfully."}
            # Packages a successful feedback boolean and string.
        except Exception as e:
        # Triggers upon MongoDB query failures.
            return {"success": False, "message": str(e)}
            # Transmits the text form of the encountered unhandled error.

    @staticmethod
    # Tags method to class not instance.
    def update_faculty(faculty_id, data):
    # Adjusts explicit faculty member details given their unique faculty ID.
        try:
        # Starts safely executed query block.
            data = capitalize_data(data)
            # Ensures new adjustments are also properly capitalized.
            db.faculty.update_one({"id": faculty_id}, {"$set": data})
            # Injects modifications straight into the targeted document via Mongo $set semantics.
            return {"success": True, "message": "Faculty updated successfully."}
            # Propagates a completed status structure.
        except Exception as e:
        # Surrounds unexpected outcomes.
            return {"success": False, "message": str(e)}
            # Failsafes and echoes back the error text.

    @staticmethod
    # Method flag.
    def delete_faculty(faculty_id):
    # Permits removing staff data from the persistence layer.
        try:
        # Execution wrapper.
            db.faculty.delete_one({"id": faculty_id})
            # Seeks out the distinct faculty ID and drops the complete stored entry.
            return {"success": True, "message": "Faculty deleted successfully."}
            # Generates completion context map.
        except Exception as e:
        # Monitors crashes.
            return {"success": False, "message": str(e)}
            # Packages crashed conditions back to handlers.

    @staticmethod
    # Denotes unattached method.
    def get_all_faculty():
    # Helper to spool out all stored faculty data natively into Python types.
        try:
        # Try bracket.
            return list(db.faculty.find({}, {"_id": 0}))
            # Instructs database to dump the faculty list, filters out underlying internal object IDs.
        except Exception:
        # Blocks crash if DB connection severs midway.
            return []
            # Assures caller loop won't exception, issuing a benign blank array.