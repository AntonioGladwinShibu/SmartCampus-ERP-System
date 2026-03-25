from config.database import db
# Imports the centralized database instance to interact with MongoDB collections.
from datetime import datetime
# Imports datetime module to attach timestamps to orders.

class CanteenService:
# Defines a class that handles business logic for adding menu items and processing orders.
    """Manages the canteen menu and orders."""
    # Docstring describing the CanteenService.
    
    @staticmethod
    # Declares the next method as static.
    def add_menu_item(item_id, name, price, quantity, category="Snacks"):
    # Defines a method to insert a new food or drink item into the canteen menu.
        try:
        # Tries to perform the insert operation.
            db.menu.insert_one({
            # Adds a single document to the 'menu' collection.
                "item_id": str(item_id).upper() if item_id else item_id,
                # Standardizes the item ID to uppercase.
                "name": str(name).upper() if name else name,
                # Standardizes the item name to uppercase string.
                "price": float(price),
                # Parses the provided price to a float value.
                "quantity": int(quantity),
                # Parses the given quantity into an integer limit.
                "category": category
                # Stores the item's overarching category grouping.
            })
            # Finalizes the dictionary document details.
            return {"success": True, "message": "Menu item added successfully."}
            # If inserted without crash, return success true object.
        except Exception as e:
        # Handles potential failures during insert.
            if "duplicate key" in str(e).lower() or getattr(e, "code", 0) == 11000:
            # specifically identifies if the failure was due to duplicate unique IDs in MongoDB.
                return {"success": False, "message": "Item ID already exists."}
                # Gives user-friendly feedback rather than throwing exception trace.
            return {"success": False, "message": str(e)}
            # Fallback error mapping for any other issues.

    @staticmethod
    # Declares static method.
    def delete_menu_item(item_id):
    # Method definitions that allows deleting an item by its designated ID.
        try:
        # Starts execution block.
            res = db.menu.delete_one({"item_id": item_id})
            # Locates and deletes the single menu document with the matching custom item_id.
            if res.deleted_count > 0:
            # Checks if the database acknowledge deleting greater than 0 documents.
                return {"success": True, "message": "Menu item deleted."}
                # Inform caller the item is scrubbed successfully.
            return {"success": False, "message": "Item not found."}
            # Tells caller that no item aligned with that ID so deletion was skipped.
        except Exception as e:
        # In case DB is offline or broken.
            return {"success": False, "message": str(e)}
            # Cast exception to string and emit.

    @staticmethod
    # Static declarator.
    def restock_item(item_id, additional_quantity):
    # Handles replenishing stock of already existing items.
        try:
        # try wrapper.
            res = db.menu.update_one(
            # Start updating query on menu collection.
                {"item_id": item_id},
                # Sets the search condition via item_id.
                {"$inc": {"quantity": int(additional_quantity)}}
                # Utilizes MongoDB $inc operator to add additional_quantity to the existing value.
            )
            # Closes update_one params.
            if res.modified_count > 0:
            # See if the database effectively changed the document.
                return {"success": True, "message": "Stock updated."}
                # Success.
            return {"success": False, "message": "Item not found."}
            # Warning that the ID targeted stock didn't exist.
        except Exception as e:
        # Catches error contexts.
            return {"success": False, "message": str(e)}
            # Bubble up error structure.

    @staticmethod
    # Static tag.
    def get_menu():
    # Helper to fetch all canteen items currently logged.
        try:
        # wrapper.
            return list(db.menu.find({}, {"_id": 0}))
            # Performs empty query find on menu, strips Mongo _id, and converts entire cursor to list.
        except Exception:
        # Catches retrieval glitches.
            return []
            # Returns empty if things broke.

    @staticmethod
    # Static.
    def checkout_cart(username, cart_items, special_instructions=""):
    # Method responsible for iterating over a cart to checkout.
        """
        cart_items should be a list of dicts: [{"item_id": "...", "quantity": X}, ...]
        """
        # Note referencing formatting expectations.
        try:
        # Begin execution flow.
            if not cart_items:
            # Checks if user attempted buying zero items.
                return {"success": False, "message": "Cart is empty."}
                # Halts logical processing.
                
            total_price = 0
            # Initiates numeric counter for the whole transaction.
            order_details = []
            # Initiates array tracker for storing comprehensive cart specs.
            
            # Verify stock for all items first to ensure atomicity conceptually
            # Comment: Verify stock for all items first to ensure atomicity conceptually
            for cart_item in cart_items:
            # Loop sequentially over each selected item.
                i_id = cart_item["item_id"]
                # Caches the current item loop ID.
                qty = int(cart_item["quantity"])
                # Extract requested quantity securely as Int.
                
                if qty <= 0: return {"success": False, "message": f"Invalid quantity for {i_id}."}
                # Blocks malicious or negative bounds inputs mid loop.
                
                db_item = db.menu.find_one({"item_id": i_id})
                # Asks the database regarding existing specifications on the item.
                if not db_item:
                # Verifies that database actually found it.
                    return {"success": False, "message": f"Item {i_id} not found."}
                    # Escapes execution returning a specific item lookup error.
                if db_item["quantity"] < qty:
                # Audits if user is attempting to purchase physically more inventory than logged.
                    return {"success": False, "message": f"Not enough stock for {db_item['name']}. Only {db_item['quantity']} available."}
                    # Explains overstock limit breach to UI.
                    
                item_total = db_item["price"] * qty
                # Calculate subtotal representing (single price x times ordered).
                total_price += item_total
                # Append subtotal incrementally upon overall transaction value.
                
                order_details.append({
                # Document snapshot configuration of individual slice of order.
                    "item_id": i_id,
                    # Stamp product ID
                    "name": db_item["name"],
                    # Stamp visual name referencing DB pull.
                    "quantity": qty,
                    # Store exact amount requested.
                    "price_per_unit": db_item["price"],
                    # Trace cost context at minute of request.
                    "item_total": item_total
                    # Trace overall chunk value.
                })
                # Ends the tracking object insertion.
                
            # If all stock checks pass, record the order
            # Comment: If all stock checks pass, record the order
            # (Stock is updated upon order completion)
            # Comment: (Stock is updated upon order completion)
                
            # Generate a unique order ID using timestamp
            # Comment: Generate a unique order ID using timestamp
            order_id = "ORD-" + datetime.now().strftime("%Y%m%d%H%M%S")
            # Leverages python time primitives for predictable sequencing based string ID.
            
            db.orders.insert_one({
            # Logs final aggregated tracking parameters into orders history.
                "order_id": order_id,
                # Stamps unique trace sequence.
                "username": username,
                # Maps buying actor.
                "items": order_details,
                # Enmeshes nested objects structure holding individual breakdowns.
                "total_price": total_price,
                # Summarizes overall final checkout burden.
                "special_instructions": special_instructions,
                # Accommodates user specific text like "extra spicy".
                "status": "Pending",
                # Initializes chronological flag signaling staff to start acting.
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Stores exact instant interaction occurred formally formatted.
            })
            # Closes final order object parameters.
            
            return {"success": True, "message": f"Checkout successful! Order ID: {order_id}"}
            # Completes cart procedure forwarding success trace ID.
        except Exception as e:
        # Safeguards generic breakdowns inside loop and outer blocks.
            return {"success": False, "message": str(e)}
            # Reports glitch to exterior calls.

    @staticmethod
    # Function modifier declaring static bound property.
    def get_orders(username=None):
    # Generates readout spanning all historically recorded checkouts, optionally filtering.
        try:
        # Safety catch blocks.
            query = {"username": username} if username else {}
            # Shorthand evaluating logic if argument provides criteria, otherwise creates blank catch-all dictionary.
            return list(db.orders.find(query, {"_id": 0}).sort("date", -1))
            # Retrieves DB orders filtering, excluding default Mongo key and descending timestamp sorting to show recent first.
        except Exception:
        # Handles broken data retrieval occurrences.
            return []
            # Exits cleanly granting empty UI instead of fatal crashes.

    @staticmethod
    # Last static declaration.
    def update_order_status(order_id, new_status):
    # Controller block addressing order lifecycle transitions handled mainly by Admin staff.
        try:
        # Safe-guard implementation wrapper.
            order = db.orders.find_one({"order_id": order_id})
            # Captures whole payload to do logic check against state changes (especially "Completed").
            if not order:
            # Handles typo-bound searches natively without throwing core Exceptions.
                return {"success": False, "message": "Order not found."}
                # Immediately dispatches missing status report back.

            res = db.orders.update_one(
            # Attempts editing of primary order document.
                {"order_id": order_id},
                # Establishes constraint against unique ID.
                {"$set": {"status": new_status}}
                # Forces explicit patch update swapping old state for new argument state.
            )
            # Exits query construct.
            if res.modified_count > 0:
            # Inspect outcome to gauge if any data indeed got written/shifted.
                if new_status == "Completed" and order.get("status") != "Completed":
                # Special logic condition checking if transaction is fully closed and wasn't originally so.
                    for item in order.get("items", []):
                    # Unpack inner item tracking list.
                        db.menu.update_one(
                        # Query modifying underlying item quantities locally.
                            {"item_id": item["item_id"]}, 
                            # Identifies exact inventory target.
                            {"$inc": {"quantity": -int(item["quantity"])}}
                            # Negative increment lowers overarching warehouse pool appropriately matching requested count.
                        )
                        # Closes nested loop query.
                return {"success": True, "message": f"Order {order_id} marked as {new_status}."}
                # Feedback loop confirms successful admin operation.
            return {"success": False, "message": "Order not found or status unchanged."}
            # Failsafe addressing instance where same status is re-applied or data vaporized mid check.
        except Exception as e:
        # Highest level handler.
            return {"success": False, "message": str(e)}
            # Broadcast stringified failure contexts natively.
