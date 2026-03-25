from config.database import db
# Imports the MongoDB database connection instance for database operations.

class AttendanceService:
# Defines the AttendanceService class that handles tracking student attendance.
    @staticmethod
    # Decorates the following method as static so it doesn't require a class instance.
    def mark_attendance(student_id, course_id, status, date):
    # Defines a method to insert or update a student's attendance record for a specific course and date.
        try:
        # Starts a try block to gracefully catch potential database exceptions.
            db.attendance.update_one(
            # Calls the update_one method on the 'attendance' collection.
                {"student_id": student_id, "course_id": course_id, "date": date},
                # Sets the search criteria: matching by student_id, course_id, and date.
                {"$set": {"status": status}},
                # Updates the 'status' field with the provided status value (e.g., 'Present', 'Absent').
                upsert=True
                # Sets upsert to True so a new record is created if no matching doc is found.
            )
            # Closes the update_one method call.
            return {"success": True, "message": "Attendance marked."}
            # Returns a success dictionary indicating the operation completed without errors.
        except Exception as e:
        # Catches any base Exception that might occur during the database operation.
            return {"success": False, "message": str(e)}
            # Returns a failure dictionary with the string representation of the exception.

    @staticmethod
    # Decorates the following method as a static method.
    def get_student_attendance(student_id):
    # Defines a method to fetch all attendance records for a specific student.
        try:
        # Starts a try block for the database query.
            return list(db.attendance.find({"student_id": student_id}, {"_id": 0}))
            # Queries the attendance collection for the student ID and converts the cursor to a list, excluding the _id field.
        except Exception:
        # Catches any potential exceptions during the lookup.
            return []
            # Returns an empty list if an exception occurs.

    @staticmethod
    # Decorates the method as static.
    def get_course_attendance(course_id):
    # Defines a method to fetch all attendance records associated with a specific course.
        try:
        # Starts a try block for the query operation.
            return list(db.attendance.find({"course_id": course_id}, {"_id": 0}))
            # Queries the database for the given course ID, excludes the _id field, and returns as a list.
        except Exception:
        # Catches any queries failures.
            return []
            # Returns an empty list if there's an error.