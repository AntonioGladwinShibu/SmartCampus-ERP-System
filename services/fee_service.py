from config.database import db
# Hooks up with the global MongoDB db reference to manage user accounts.

class FeeService:
# Describes the primary component responsible for tuitions management tracking.
    """Manages student tuition and fee payments."""
    # Summarized docstring declaring purpose.
    
    @staticmethod
    # States the method belongs generically to the namespace.
    def record_payment(student_username, amount, semester, status="Pending"):
    # Commits a foundational payment record that students need to settle.
        try:
        # Traps faults.
            db.fees.insert_one({
            # Inlines a new payment tracking block to the fees collection.
                "student_username": student_username,
                # Records string name representing which student owes balance.
                "amount": amount,
                # Notates the numeric financial burden expected.
                "semester": semester,
                # Notates specific term the bill corresponds towards.
                "status": status
                # Notes starting condition, generally defaulting to Pending.
            })
            # Seals dictionary bounds.
            return {"success": True, "message": "Fee payment recorded."}
            # Sends confirming context struct.
        except Exception as e:
        # Resolves database insert blocks.
            return {"success": False, "message": str(e)}
            # Forwards exact trace descriptions wrapped safely.

    @staticmethod
    # Binds statically.
    def pay_fee(student_username, semester):
    # Marks out an existing debt ledger as formally Paid.
        try:
        # Encapsulates code.
            res = db.fees.update_one(
            # Tells collection to look up specific tuple then overwrite statuses.
                {"student_username": student_username, "semester": semester},
                # Narrows modification scope leveraging unique user + semester combination.
                {"$set": {"status": "Paid"}}
                # Asserts patch action.
            )
            # Resolves query context.
            if res.modified_count > 0:
            # Assesses if query modified document or if it was already marked so.
                return {"success": True, "message": "Fee marked as Paid."}
                # Successful confirmation map.
            return {"success": False, "message": "Fee record not found or already paid."}
            # Notice implying lack of corresponding doc update.
        except Exception as e:
        # Crash trap.
            return {"success": False, "message": str(e)}
            # Forward error log.

    @staticmethod
    # Marker.
    def get_student_fees(student_username):
    # Generates a historical roster of all tuition records relative to one username.
        try:
        # Safety.
            return list(db.fees.find({"student_username": student_username}, {"_id": 0}))
            # Looks strictly for those files tagged with the passed student string, drops _id, and lists them.
        except Exception:
        # Failsafe execution.
            return []
            # Grants an empty placeholder upon crash to not disrupt loops visually.
            
    @staticmethod
    # Independent function tag.
    def get_unpaid_students(semester):
    # Identifies all students falling under delinquency relative to a specified term.
        try:
        # Operation safety net.
            # Simple check for students without a "Paid" record in the semantic semester
            # Comment: Simple check for students without a "Paid" record in the semantic semester
            paid_students = db.fees.distinct("student_username", {"semester": semester, "status": "Paid"})
            # Assembles array aggregating exactly who has finalized term debts.
            all_students = db.users.find({"role": "STUDENT"})
            # Pulls an unadulterated listing representing all valid active students system-wide.
            
            unpaid = [s for s in all_students if s.get("username") not in paid_students]
            # Loops comprehensions cross-referencing all users against the previously built paid_students array.
            # Removing _id for safety
            # Comment: Removing _id for safety
            for s in unpaid:
            # Stepwise iterations upon unpaid dict objects modifying them actively in memory.
                if "_id" in s:
                # Double checks whether ObjectId exists on object string representations natively.
                    del s["_id"]
                    # Erases that Object ID natively from dictionary pointer list item to avert casting defects upon UI view binding.
                    
            return unpaid
            # Returns synthesized clean mapping array displaying precisely indebted users.
        except Exception as e:
        # Wraps block unhandled occurrences elegantly.
            return []
            # Submits benign payload.