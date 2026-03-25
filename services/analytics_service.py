class AnalyticsService:
# Defines the AnalyticsService class to handle fetching summary statistics for the dashboard.
    @staticmethod
    # Declares the following method as a static method so it can be called without instantiating the class.
    def get_summary_stats():
    # Defines the method 'get_summary_stats' to retrieve counts of various entities.
        from config.database import db
        # Imports the database connection locally to avoid circular dependencies.
        return {
        # Returns a dictionary containing the count statistics.
            "students": db.users.count_documents({"role": "STUDENT"}),
            # Queries the 'users' collection to count how many documents have the role "STUDENT".
            "faculty": db.users.count_documents({"role": "FACULTY"}),
            # Queries the 'users' collection to count how many documents have the role "FACULTY".
            "courses": db.courses.count_documents({}),
            # Counts the total number of documents in the 'courses' collection.
            "books": db.library.count_documents({})
            # Counts the total number of documents in the 'library' collection.
        }
        # Ends the dictionary definition.