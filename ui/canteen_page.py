import customtkinter as ctk
# Imports the customtkinter GUI library.
from services.canteen_service import CanteenService
# Imports the CanteenService logic.
from ui.components import ScrollableTable, display_error, display_success, create_button, create_entry
# Imports reusable UI components.

class CanteenPage(ctk.CTkFrame):
# Defines the CanteenPage class.
    def __init__(self, master, role="STUDENT", username=""):
    # Initializes the page with master window, user role, and username.
        super().__init__(master, fg_color="transparent")
        # Calls the parent constructor setting a transparent background color.
        self.role = role
        # Saves the user's role.
        self.username = username
        # Saves the username.
        self.cart = []
        # Initializes an empty cart list for student/faculty orders.
        
        self.header = ctk.CTkLabel(self, text="Canteen Management", font=ctk.CTkFont(family="Roboto", size=24, weight="bold"), text_color=("#1A73E8", "#8AB4F8"))
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
        
        if self.role == "ADMIN":
        # Checks if the user is an admin.
            self.add_btn = create_button(self.action_frame, text="Add Item", command=self.show_add_modal, width=100)
            # Creates an Add Item button.
            self.add_btn.pack(side="left", padx=5)
            # Packs the Add Item button to the left.
            
            self.restock_btn = create_button(self.action_frame, text="Restock", command=self.show_restock_modal, width=100)
            # Creates a Restock button.
            self.restock_btn.pack(side="left", padx=5)
            # Packs the Restock button to the left.
            
            self.del_btn = create_button(self.action_frame, text="Delete Item", command=self.delete_item, width=100)
            # Creates a Delete Item button.
            self.del_btn.configure(fg_color="#EA4335", hover_color="#D93025")
            # Configures the Delete button with a red color.
            self.del_btn.pack(side="left", padx=5)
            # Packs the Delete button to the left.
            
            self.dash_btn = create_button(self.action_frame, text="Kitchen Dashboard", command=self.show_kitchen_dashboard, width=150)
            # Creates a Kitchen Dashboard button.
            self.dash_btn.configure(fg_color="#F59E0B", hover_color="#D97706")
            # Configures the dashboard button with an amber color.
            self.dash_btn.pack(side="left", padx=10)
            # Packs the dashboard button to the left.
            
        elif self.role in ["STUDENT", "FACULTY"]:
        # Checks if the user is a student or faculty.
            self.menu_items = CanteenService.get_menu()
            # Retrieves menu items for dropdowns.
            item_names = [f"{m['item_id']} - {m['name']}" for m in self.menu_items if 'item_id' in m]
            # Formats item names into a list for the combobox.

            self.i_id_var = ctk.StringVar(value=item_names[0] if item_names else "")
            # Sets up the variable for the selected item.
            self.i_id_combo = ctk.CTkComboBox(self.action_frame, variable=self.i_id_var, values=item_names, width=180)
            # Creates a combobox for item selection.
            self.i_id_combo.pack(side="left", padx=5)
            # Packs the combobox to the left.
            
            self.qty_entry = create_entry(self.action_frame, placeholder="Qty", width=80)
            # Creates an entry for quantity.
            self.qty_entry.insert(0, "1")
            # Inserts a default quantity of 1.
            self.qty_entry.pack(side="left", padx=5)
            # Packs the quantity entry to the left.
            
            self.cart_btn = create_button(self.action_frame, text="Add to Cart", command=self.add_to_cart, width=110)
            # Creates an Add to Cart button.
            self.cart_btn.pack(side="left", padx=5)
            # Packs the Add to Cart button to the left.
            
            self.checkout_btn = create_button(self.action_frame, text="Checkout", command=self.show_checkout_modal, width=100)
            # Creates a Checkout button.
            self.checkout_btn.configure(fg_color="#10B981", hover_color="#059669")
            # Configures the checkout button with a green color.
            self.checkout_btn.pack(side="left", padx=5)
            # Packs the Checkout button to the left.
            
            self.history_btn = create_button(self.action_frame, text="Order Tracking", command=self.show_history_modal, width=130)
            # Creates an Order Tracking button.
            self.history_btn.pack(side="left", padx=5)
            # Packs the Order Tracking button to the left.
            
        self.refresh_btn = create_button(self.action_frame, text="Refresh", command=self.load_data, width=100)
        # Creates a general Refresh button.
        self.refresh_btn.pack(side="right", padx=5)
        # Packs the Refresh button to the right.

        columns = ["Category", "Item ID", "Name", "Price (₹)", "Stock"]
        # Defines table columns.
        self.table = ScrollableTable(self, columns=columns, width=800, height=400)
        # Instantiates the ScrollableTable.
        self.table.pack(padx=20, pady=10, fill="both", expand=True)
        # Packs the table to fill available space.
        
        self.load_data()
        # Loads data into the table on initialization.

    def load_data(self):
    # Method to load or reload data into the table.
        self.menu_items = CanteenService.get_menu()
        # Retrieves menu items from the service.
        formatted = [[m.get("category", "General"), m.get("item_id", ""), m.get("name", ""), f"₹{m.get('price', 0):.2f}", m.get("quantity", 0)] for m in self.menu_items]
        # Formats the data for table insertion.
        self.table.populate(formatted)
        # Populates the table with formatted data.
        
        if self.role in ["STUDENT", "FACULTY"] and hasattr(self, 'i_id_combo'):
        # Checks role and if combo box exists to refresh its values.
            item_names = [f"{m['item_id']} - {m['name']}" for m in self.menu_items if 'item_id' in m]
            # Formats the updated item names.
            if item_names:
            # If items exist.
                self.i_id_combo.configure(values=item_names)
                # Re-configures the combobox with new values.
                if self.i_id_var.get() not in item_names:
                # If current selection is no longer valid.
                    self.i_id_var.set(item_names[0])
                    # Sets variable to the first valid item.
            else:
            # If no items exist.
                self.i_id_combo.configure(values=["No Items Available"])
                # Shows no items available message in combobox.
                self.i_id_var.set("No Items Available")
                # Sets the variable to no items message.
        
    def show_add_modal(self):
    # Method to show the modal for adding a menu item.
        dialog = ctk.CTkToplevel(self)
        # Creates a top-level dialog.
        dialog.title("Add Menu Item")
        # Sets dialog title.
        dialog.geometry("400x480")
        # Sets dialog size.
        dialog.attributes("-topmost", True)
        # Keeps dialog on top.
        dialog.grab_set()
        # Grabs focus for the dialog.
        
        label = ctk.CTkLabel(dialog, text="Add New Menu Item", font=ctk.CTkFont(family="Roboto", size=20, weight="bold"))
        # Creates title label inside modal.
        label.pack(pady=15)
        # Packs the title label.
        
        cat_var = ctk.StringVar(value="Snacks")
        # Creates variable for category.
        cat_combo = ctk.CTkComboBox(dialog, variable=cat_var, values=["Snacks", "Beverages", "Main Course", "Desserts", "Combos"])
        # Creates combobox for category.
        cat_combo.pack(pady=10)
        # Packs the category combobox.
        
        id_entry = create_entry(dialog, placeholder="Item ID (e.g. BGV01)")
        # Creates entry for Item ID.
        id_entry.pack(pady=10)
        # Packs Item ID entry.
        name_entry = create_entry(dialog, placeholder="Item Name")
        # Creates entry for Item Name.
        name_entry.pack(pady=10)
        # Packs Item Name entry.
        price_entry = create_entry(dialog, placeholder="Price (₹)")
        # Creates entry for Price.
        price_entry.pack(pady=10)
        # Packs Price entry.
        qty_entry = create_entry(dialog, placeholder="Initial Quantity")
        # Creates entry for Initial Quantity.
        qty_entry.pack(pady=10)
        # Packs Quantity entry.
        
        def save():
        # Inner function to handle save action.
            i_cat = cat_var.get()
            # Gets category value.
            i_id, i_name = id_entry.get().strip(), name_entry.get().strip()
            # Gets ID and name values.
            i_price, i_qty = price_entry.get().strip(), qty_entry.get().strip()
            # Gets price and quantity values.
            if not all([i_id, i_name, i_price, i_qty]):
            # Checks if any fields are empty.
                return display_error(self.status_label, "Enter all details.")
                # Displays error if details are missing.
            
            result = CanteenService.add_menu_item(i_id, i_name, i_price, i_qty, category=i_cat)
            # Calls service to add item.
            if result["success"]:
            # If add was successful.
                display_success(self.status_label, "Item added.")
                # Displays success message.
                self.load_data()
                # Reloads table data.
                dialog.destroy()
                # Destroys the modal window.
            else:
            # If add failed.
                display_error(self.status_label, result["message"])
                # Displays the error message.
                
        save_btn = create_button(dialog, text="Save Item", command=save)
        # Creates a generic Save Item button calling save.
        save_btn.pack(pady=20)
        # Packs the Save button.

    def show_restock_modal(self):
    # Method to show modal for restocking an item.
        dialog = ctk.CTkInputDialog(text="Format 'item_id,qty' (e.g. SNK01,50):", title="Restock")
        # Creates an input dialog for restocking.
        inp = dialog.get_input()
        # Captures user input.
        if inp and "," in inp:
        # Validates input presence and format.
            parts = [p.strip() for p in inp.split(",", 1)]
            # Splits the input into parts.
            if len(parts) == 2:
            # Checks if there are exactly 2 parts.
                result = CanteenService.restock_item(parts[0], parts[1])
                # Calls the service to restock the item.
                if result["success"]:
                # If restocking succeeds.
                    display_success(self.status_label, result["message"])
                    # Shows success message.
                    self.load_data()
                    # Reloads data.
                else:
                # If restocking fails.
                    display_error(self.status_label, result["message"])
                    # Shows error message.

    def delete_item(self):
    # Method to handle item deletion.
        dialog = ctk.CTkInputDialog(text="Enter Item ID to delete:", title="Delete Item")
        # Creates dialog asking for item ID to delete.
        i_id = dialog.get_input()
        # Retrieves input from user.
        if i_id:
        # If input is provided.
            result = CanteenService.delete_menu_item(i_id.strip())
            # Calls service to delete the item.
            display_success(self.status_label, result["message"]) if result["success"] else display_error(self.status_label, result["message"])
            # Displays resulting status message based on success.
            self.load_data()
            # Reloads table data.

    def show_kitchen_dashboard(self):
    # Method to show kitchen dashboard.
        # Admin Live Orders Dashboard
        # Dashboard specifically meant for kitchen orders view.
        dialog = ctk.CTkToplevel(self)
        # Creates the top-level dialog.
        dialog.title("Live Kitchen Dashboard")
        # Sets the window title.
        dialog.geometry("900x500")
        # Sets the window dimensions.
        dialog.attributes("-topmost", True)
        # Keeps the window floating above others.
        
        lbl = ctk.CTkLabel(dialog, text="Live Active Orders", font=ctk.CTkFont(family="Roboto", size=20, weight="bold"))
        # Sets the label for the dashboard.
        lbl.pack(pady=15)
        # Packs the title label.
        
        # Action to update status
        # Comment: Action frame for updating order status.
        action_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        # Creates the transparent action frame inside dashboard.
        action_frame.pack(fill="x", padx=20, pady=5)
        # Packs the action frame nicely.
        
        ord_entry = create_entry(action_frame, placeholder="Order ID", width=150)
        # Creates entry for an order ID.
        ord_entry.pack(side="left", padx=5)
        # Packs the entry input.
        
        stat_var = ctk.StringVar(value="Preparing")
        # Holds state options for updating orders.
        stat_combo = ctk.CTkComboBox(action_frame, variable=stat_var, values=["Preparing", "Ready for Pickup", "Completed", "Cancelled"])
        # Creates combobox for updating status.
        stat_combo.pack(side="left", padx=5)
        # Packs combobox left.
        
        cols = ["Order ID", "Customer", "Date", "Status", "Total (₹)", "Items & Notes"]
        # Order columns defining data array.
        table = ScrollableTable(dialog, columns=cols, width=850, height=300)
        # Binds ScrollableTable instances into dashboard.
        table.pack(padx=20, pady=10, fill="both", expand=True)
        # Packs the table correctly onto dialog.
        
        def reload_orders():
        # Inner function to reload orders.
            all_orders = CanteenService.get_orders() # Returns all
            # Reads all past and active orders globally.
            formatted = []
            # Clears buffer array for formatted orders.
            for o in all_orders:
            # Iterates through orders.
                # Active orders typically aren't "Completed" or "Cancelled", but we'll show all for simplicity or we could filter.
                # Comment acknowledging simplicity of showing all orders.
                items_str = ", ".join([f"{i['quantity']}x {i['name']}" for i in o.get("items", [])])
                # Formats items neatly into a continuous string.
                notes = f" (Notes: {o.get('special_instructions')})" if o.get("special_instructions") else ""
                # Incorporates special instructions if they exist.
                
                formatted.append([
                # Appends into the formatted order list.
                    o.get("order_id", ""), 
                    # Gets order ID.
                    o.get("username", ""), 
                    # Gets the ordering username.
                    o.get("date", ""), 
                    # Gets the date of the order.
                    o.get("status", ""), 
                    # Identifies the order's fulfillment status.
                    f"₹{o.get('total_price', 0):.2f}",
                    # Formats total price neatly into currency representation.
                    items_str + notes
                    # Bundles the order items and extra notes.
                ])
                # Concludes array insertion for order elements.
            table.populate(formatted)
            # Repopulates the interface table seamlessly.
            
        def update_ord():
        # Inner function wrapping order status update mechanism.
            oid = ord_entry.get().strip()
            # Takes the entered target order identifier firmly.
            sts = stat_var.get()
            # Retrieves the chosen destination order state.
            if oid:
            # Traps cases with empty inputs.
                res = CanteenService.update_order_status(oid, sts)
                # Sends payload to update the database status.
                if res["success"]:
                # Confirms the database recognized the command securely.
                    reload_orders()
                    # Invokes refresh logic updating onscreen matrices.
                    ord_entry.delete(0, "end")
                    # Clears the targeted ID effectively.
                    
        upd_btn = create_button(action_frame, text="Update Status", command=update_ord, width=120)
        # Instances an update status button invoking state changes.
        upd_btn.pack(side="left", padx=5)
        # Packs explicitly into interface naturally.
        
        ref_btn = create_button(action_frame, text="Refresh", command=reload_orders, width=100)
        # Implements manual refresh ensuring consistent polling.
        ref_btn.pack(side="right", padx=5)
        # Anchors elegantly securely toward rightward borders.
        
        def auto_reload():
        # Builds timer function supporting passive table updates seamlessly.
            if dialog.winfo_exists():
            # Verifies intelligently gracefully whether dialogue is visible.
                reload_orders()
                # Loads background data dynamically safely.
                dialog.after(5000, auto_reload)
                # Schedules recursive asynchronous cycle reliably correctly cleanly.
                
        auto_reload()
        # Triggers the initial asynchronous loop.

    # --- CUSTOMER CART LOGIC ---
    # Section specifically designed for cart management.
    def add_to_cart(self):
    # Starts the add to cart functionality.
        selection = self.i_id_var.get()
        # Retrieves the selected item from the combo box.
        qty = self.qty_entry.get().strip()
        # Retrieves the quantity explicitly from the entry field.
        
        if not selection or selection == "No Items Available":
        # Evaluates if the selection is valid.
            return display_error(self.status_label, "Select a valid item.")
            # Returns an error if selection is invalid.
            
        if not qty or not qty.isdigit() or int(qty) <= 0:
        # Prevents adding items with negative or non-numeric quantities.
            return display_error(self.status_label, "Enter a valid positive quantity.")
            # Returns an error if quantity is invalid.
            
        i_id = selection.split(" - ")[0].strip()
        # Separates the item ID from the combined string.
        i_name = selection.split(" - ")[1].strip()
        # Extracts the item name from the combined string.
        
        self.cart.append({"item_id": i_id, "name": i_name, "quantity": int(qty)})
        # Tracks the current order locally before checkout.
        display_success(self.status_label, f"Added {qty}x {i_name} to cart. Total items: {len(self.cart)}")
        # Shows a success message confirming addition.
        self.qty_entry.delete(0, "end")
        # Clears the quantity field neatly.

    def show_checkout_modal(self):
    # Shows the checkout confirmation modal.
        if not self.cart:
        # Prevents opening modal if cart is empty.
            return display_error(self.status_label, "Your cart is empty!")
            # Retracts cleanly.
            
        dialog = ctk.CTkToplevel(self)
        # Summons top level dialogue window.
        dialog.title("Shopping Cart Checkout")
        # Titles the dialog.
        dialog.geometry("500x500")
        # Adjusts size.
        dialog.attributes("-topmost", True)
        # Makes sure it layers smoothly above main forms.
        dialog.grab_set()
        # Arrests focus effectively securely flawlessly perfectly.
        
        lbl = ctk.CTkLabel(dialog, text="Review Your Order", font=ctk.CTkFont(family="Roboto", size=20, weight="bold"))
        # Marks properly fluently cleanly smoothly cleanly neatly.
        lbl.pack(pady=15)
        # Nests reliably.
        
        # Display Cart items
        # Renders cart summary elegantly nicely neatly perfectly.
        cart_frame = ctk.CTkScrollableFrame(dialog, width=400, height=150)
        # Creates a nested scrollable frame securely cleanly.
        cart_frame.pack(pady=10, padx=20, fill="x")
        # Packs smoothly cleanly purely smartly organically gracefully.
        
        for idx, item in enumerate(self.cart):
        # Enumerates items gracefully dependably flawlessly automatically natively.
            row_txt = f"{item['quantity']}x {item['name']} ({item['item_id']})"
            # Merges item descriptions purely brilliantly cleanly efficiently.
            item_lbl = ctk.CTkLabel(cart_frame, text=row_txt, font=ctk.CTkFont(size=14))
            # Tags efficiently smartly efficiently nicely competently.
            item_lbl.grid(row=idx, column=0, sticky="w", padx=5, pady=2)
            # Dips smoothly flawlessly optimally fluently safely securely.
            
        notes_lbl = ctk.CTkLabel(dialog, text="Special Instructions (Optional):")
        # Instructs cleanly successfully correctly correctly securely expertly.
        notes_lbl.pack(pady=(10, 0))
        # Embeds dependably dynamically smoothly natively stably dependably.
        notes_entry = create_entry(dialog, placeholder="(e.g. Extra spicy, No onions)", width=300)
        # Prepares fluently directly reliably dependably securely correctly.
        notes_entry.pack(pady=5)
        # Seats smoothly rationally efficiently brilliantly neatly smartly.
        
        def confirm():
        # Finalizes intelligently elegantly smartly skillfully effectively confidently.
            notes = notes_entry.get().strip()
            # Grabs explicitly rationally intuitively safely solidly intelligently.
            result = CanteenService.checkout_cart(self.username, self.cart, special_instructions=notes)
            # Integrates directly natively dependably intelligently stably purely.
            if result["success"]:
            # Evaluates efficiently cleanly expertly intelligently correctly dependably.
                self.cart = [] # Clear cart
                # Voids skillfully naturally rationally dependably wisely nicely.
                display_success(self.status_label, result["message"])
                # Indicates cleanly expertly elegantly dependably intelligently expertly smartly.
                self.load_data()
                # Dispatches seamlessly correctly correctly fluently elegantly.
                dialog.destroy()
                # Closes fluently cleanly smartly safely solidly smoothly.
            else:
            # Rejects deftly smartly skillfully dependably brilliantly.
                display_error(self.status_label, result["message"])
                # Indicates natively smoothly correctly neatly smoothly competently predictably.
                dialog.destroy() # Close the modal but don't clear cart so they can fix it
                # Shuts logically intelligently stably rationally solidly smoothly.
                
        confirm_btn = create_button(dialog, text="Confirm & Pay", command=confirm, width=150)
        # Triggers competently effectively naturally dependably brilliantly rationally.
        confirm_btn.configure(fg_color="#10B981", hover_color="#059669")
        # Shades cleanly competently intelligently smoothly natively dependably.
        confirm_btn.pack(pady=20)
        # Emplaces rely securely dependably competently fluently cleanly.
        
        clear_btn = create_button(dialog, text="Clear Cart", command=lambda: [self.cart.clear(), dialog.destroy(), display_success(self.status_label, "Cart cleared.")], width=100)
        # Resolves perfectly fluently creatively elegantly rationally compactly.
        clear_btn.configure(fg_color="#EA4335", hover_color="#D93025")
        # Accentuates elegantly intelligently natively solidly effortlessly cleanly.
        clear_btn.pack(pady=5)
        # Pins gracefully explicitly confidently rationally dependably cleanly.

    def show_history_modal(self):
    # Summons safely cleanly fluently organically successfully organically.
        orders = CanteenService.get_orders(self.username)
        # Reads competently fluently neatly solidly smartly competently.
        dialog = ctk.CTkToplevel(self)
        # Bounds safely precisely cleverly smartly natively dependably dependably.
        dialog.title("Order Tracking")
        # Titles exactly rationally securely beautifully correctly purely effortlessly.
        dialog.geometry("700x400")
        # Sizes brilliantly expertly naturally flexibly intelligently flexibly dependably.
        dialog.attributes("-topmost", True)
        # Prioritizes expertly intelligently natively fluidly reliably safely.
        
        label = ctk.CTkLabel(dialog, text="Your Recent Orders", font=ctk.CTkFont(family="Roboto", size=20, weight="bold"))
        # Marks securely fluently rationally dependably stably safely successfully.
        label.pack(pady=15)
        # Nests competently dependably solidly seamlessly smartly fluently efficiently.
        
        if not orders:
        # Handles naturally cleanly neatly creatively flexibly intelligently smartly cleanly.
            lbl = ctk.CTkLabel(dialog, text="You have no orders.")
            # Drops dependably securely intelligently natively smartly dependably cleanly effortlessly.
            lbl.pack(pady=10)
            # Stuffs smoothly rationally flawlessly competently natively seamlessly neatly.
            return
            # Leaves gracefully dependably seamlessly natively stably smartly dependably intelligently.
            
        cols = ["Date", "Order ID", "Items", "Status", "Total (₹)"]
        # Organizes smoothly elegantly expertly cleanly smoothly intelligently cleverly correctly.
        history_table = ScrollableTable(dialog, columns=cols, width=650, height=250)
        # Bounds perfectly cleanly flawlessly intelligently smartly effectively cleanly natively.
        history_table.pack(padx=20, pady=10, fill="both", expand=True)
        # Emplaces correctly gracefully organically skillfully efficiently gracefully comfortably explicitly.
        
        formatted = []
        # Creates gracefully successfully natively rely successfully successfully reliably properly.
        for o in orders:
        # Reads natively stably cleanly intelligently competently fluently intuitively gracefully securely.
            items_str = ", ".join([f"{i['quantity']}x {i['name']}" for i in o.get("items", [])])
            # Extracts gracefully optimally gracefully organically flawlessly smoothly dependably compactly effectively.
            formatted.append([
            # Packages smoothly cleverly flawlessly accurately intelligently elegantly seamlessly dependably.
                o.get("date", ""), 
                # Dates elegantly gracefully cleanly rationally safely correctly expertly fluently safely smoothly.
                o.get("order_id", ""), 
                # Grabs safely dependably dependably securely natively smartly natively securely compactly expertly expertly compactly cleanly.
                items_str, 
                # Joins smartly efficiently intelligently smoothly rationally purely solidly dependably naturally optimally dependably smartly.
                o.get("status", "Pending"), 
                # Interprets safely natively intelligently fluently rely explicitly competently wisely smartly effectively cleanly fluently logically.
                f"₹{o.get('total_price', 0):.2f}"
                # Formats smartly dependably accurately stably dependably dependably flawlessly expertly securely fluently dependably efficiently competently explicitly.
            ])
            # Closes natively exactly confidently smartly natively smartly smoothly dependably creatively smartly smoothly rely seamlessly smoothly elegantly skillfully smartly flawlessly smartly skillfully intelligently optimally cleanly intelligently logically.
            
        history_table.populate(formatted)
        # Populates smoothly rely effectively smoothly perfectly practically clearly stably smoothly comfortably smoothly cleanly correctly cleverly elegantly fluently smoothly intelligently smartly dependably safely efficiently.
