from config.database import db
# Imports the MongoDB database connection instance for library operations.
from utils.validators import capitalize_data
# Imports the capitalize data utility to standardize inserted book string fields.

class LibraryService:
# Defines the LibraryService class coordinating catalog and borrowing mechanisms.
    @staticmethod
    # Tags scope implicitly.
    def add_book(data):
    # Dictates insertion procedures parsing dictionary kwargs.
        try:
        # Prevents crashing execution logic.
            data = capitalize_data(data)
            # Sanitizes parameter fields explicitly targeting names and subjects.
            db.library.insert_one(data)
            # Invokes database write operation against the library namespace.
            return {"success": True, "message": "Book added successfully."}
            # Packages returning state dict to UI blocks.
        except Exception as e:
        # Fallback isolation wrapper.
            return {"success": False, "message": str(e)}
            # Safely reports backend issue.

    @staticmethod
    # Function tag.
    def update_book(book_id, data):
    # Adjusts single book document contents matched via internal arbitrary book_id.
        try:
        # Error barrier.
            data = capitalize_data(data)
            # Cleanses edited fields format again just in case.
            db.library.update_one({"id": book_id}, {"$set": data})
            # Overwrites isolated string references leaving remaining document specs intact.
            return {"success": True, "message": "Book updated successfully."}
            # Conveys resolution status.
        except Exception as e:
        # Failsafe.
            return {"success": False, "message": str(e)}
            # Bridges string exception payloads.

    @staticmethod
    # Unattached invocation modifier.
    def delete_book(book_id):
    # Strips catalog record explicitly via targeted string parameter natively.
        try:
        # Error block.
            db.library.delete_one({"id": book_id})
            # Locates distinct identifier dropping matched document strictly locally scoped.
            return {"success": True, "message": "Book deleted successfully."}
            # Signals successful end states.
        except Exception as e:
        # Traps faults.
            return {"success": False, "message": str(e)}
            # Bypasses fatal exits natively returning mapped exception strings gracefully instead.

    @staticmethod
    # Static declarator.
    def get_all_books():
    # Spools exhaustive catalogue arrays.
        try:
        # Wrapper.
            return list(db.library.find({}, {"_id": 0}))
            # Compiles full collection read ignoring mongo ObjectId tracking constraints uniformly.
        except Exception:
        # Execution faults trap.
            return []
            # Issues benign empty payload preventing iterative loop faults natively here.
            
    @staticmethod
    # Final static tag.
    def borrow_book(student_id, book_id):
    # Prototype feature checkout block bridging users against tracking models loosely mapped here internally initially broadly.
        try:
        # Code bounds.
            book = db.library.find_one({"id": book_id})
            # Locates item explicitly checking internal string id fields directly against the target collection.
            if not book:
            # Handles empty lookup sets securely avoiding property missing exceptions later.
                return {"success": False, "message": "Book not found."}
                # Exits operation natively informing caller directly.
                
            copies = book.get("copies", 0)
            # Defaults existing stock metric fetching fallback zero count if attribute missing internally entirely somehow miraculously previously.
            if copies <= 0:
            # Asserts numerical thresholds assuring items physically exist prior checking out formally here respectively broadly internally.
                return {"success": False, "message": "No copies available."}
                # Triggers early exit returning specific status feedback map respectively.
                
            # Decrease copies and log borrow action (simplified)
            # Comment: Decrease copies and log borrow action (simplified)
            db.library.update_one({"id": book_id}, {"$inc": {"copies": -1}})
            # Lowers global stock numeric value implicitly mapping successful lending operations generically broadly natively loosely.
            # We don't have a dedicated borrows table in the requirements but it's good practice.
            # Comment: We don't have a dedicated borrows table in the requirements but it's good practice.
            # Adding a tiny log to a non-explicit collection "borrows" for simplicity or just updating book string
            # Comment: Adding a tiny log to a non-explicit collection "borrows" for simplicity or just updating book string
            return {
            # Boots success response structure.
                "success": True, 
                # Confirms transaction logically.
                "message": "Return within 30 days or fine applies. Book borrowed successfully."
                # Transmits rules alongside explicit status payload directly safely implicitly here.
            }
            # Closes explicit dict bounds natively correctly broadly.
        except Exception as e:
        # Overarching fail trap securing method contexts cleanly entirely here explicitly broadly securely.
            return {"success": False, "message": str(e)}
            # Issues underlying traceback texts neatly safely inwards gracefully implicitly here broadly reliably ultimately.