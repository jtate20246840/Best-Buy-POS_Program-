class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, quantity):
        """Update product stock after purchase"""
        self.stock -= quantity

    def __str__(self):
        return f"{self.name} (${self.price}, Stock: {self.stock})"

class ShoppingCart:
    def __init__(self):
        self.items = {}  # Dictionary: {Product: quantity}

    def add_item(self, product, quantity,):
        """Add product to cart with quantity"""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        current_in_cart = self.items.get(product,0)
        would_be_total = current_in_cart + quantity

        if product.stock < quantity:
            raise ValueError(f"Insufficient stock. Only {product.stock} available")

        if product.stock < would_be_total:
            available = product.stock - current_in_cart
            raise ValueError (f"Cannot Add {quantity}. Only {available} more available")

        self.items[product] = would_be_total

    def remove_item(self, product, quantity):
        """Remove product from cart"""
        if product not in self.items:
            raise ValueError("Product not in cart")

        if quantity > self.items[product]:
            raise ValueError(f"Cannot remove more than {self.items[product]} items")

        self.items[product] -= quantity
        if self.items[product] == 0:
            del self.items[product]

    def calculate_subtotal(self):
        """Calculate total before tax"""
        return sum(product.price * quantity for product, quantity in self.items.items())

    def view_cart(self):
        """Display cart contents"""
        if not self.items:
            print("Your cart is empty")
            return
        print("\n***************************** BESTBUY SHOPPING CART *****************************\n")
        print("{:<25} {:<12} {:<12} {:<12}".format("Product", "Price", "Qty", "Total"))
        for product, quantity in self.items.items():
            print(f"{product.name:<25} ${product.price:<11.2f} {quantity:<12} ${product.price * quantity:<11.2f}")
        print(f"\nSUBTOTAL: ${self.calculate_subtotal():.2f}")

class POSSystem:
    def __init__(self):
        self.products = self.initialize_products()
        self.cart = ShoppingCart()

    @classmethod
    def initialize_products(cls):
        """Create initial product catalog"""
        return [
            Product("Gain Laundry Detergent", 3950, 10),
            Product("Paper Towels Bundle", 2200, 15),
            Product("Tissues - Pack of 24", 995, 20),
            Product("Large Trash Bags - Pack Size 120", 1600, 10),
            Product("ZipLock Bags - Pack Size 12", 1200, 25),
            Product("Special K Cereal Chocolate", 1700, 16),
            Product("Exotic Spices Bundle", 800, 8),
            Product("Moscato Wine", 4050, 5),
            Product("Fresh Product Combo", 1820, 12),
            Product("Exotic Breakfast Combo", 2990, 6)]

    def display_products(self):
        """Show available products"""
        print("\n*************************** BESTBUY PRODUCT CATALOG ****************************\n")
        for idx, product in enumerate(self.products, 1): # The enumerate function and the idx (index) variable works together to create a numbered product menu for a smooth user selection.
            stock_alert = " (LOW STOCK!)" if product.stock < 5 else ""
            print(f"{idx}. {product}{stock_alert}")

    def add_to_cart(self):
        """Add selected product to cart with real-time stock updates"""
        self.display_products()
        try:
            print("")
            choice = int(input("Enter product number: "))
            print("")
            if choice < 1 or choice > 10:
                raise ValueError("Invalid product number. Please enter a numeric value 1-10")

            product = self.products[choice - 1]
            try:
                # Calculate initial available quantity
                current_in_cart = self.cart.items.get(product, 0)
                available = product.stock - current_in_cart

                if available <= 0:
                    print(f"\nThis product is completely allocated (Stock: {product.stock})")
                    return

                print(f"Current stock: {product.stock}")
                print(f"Already in cart: {current_in_cart}")

                while True:
                    print(f"\nAvailable to add: {available}")
                    quantity = int(input("Enter quantity to add (0 to cancel): "))

                    if quantity == 0:
                        print("Operation cancelled")
                        return
                    if quantity < 0:
                        print("Error: Quantity cannot be negative")
                        continue
                    if quantity > available:
                        print(f"Error: Only {available} available")
                        continue

                    # Add to cart and show updated availability
                    self.cart.add_item(product, quantity)
                    new_in_cart = self.cart.items[product]
                    new_available = product.stock - new_in_cart

                    print(f"\nAdded {quantity} {product.name}(s) to cart")
                    print(f"New quantities:")
                    print(f"- In cart: {new_in_cart}")
                    print(f"- Remaining available: {new_available}")
                    break

            except ValueError:
                print("\nError: Please enter a valid number")

        except ValueError:
            print("\nError: Please enter a valid product number (1-10)")

    def remove_from_cart(self):
        """Remove item from cart"""
        self.cart.view_cart()
        if not self.cart.items:
            return

        try:
            print("\nItems in cart:\n")
            # Display numbered list of cart items
            for idx, (product, quantity) in enumerate(self.cart.items.items(), 1):
                print(f"{idx}. {product.name} (Qty: {quantity})")

            # Get item selection by number
            print("")
            item_num = int(input("Enter item number to remove: ")) - 1
            print("")
            product = list(self.cart.items.keys())[item_num]

            # Get quantity to remove
            max_quantity = self.cart.items[product]
            quantity = int(input(f"Enter quantity to remove (1-{max_quantity}): "))

            self.cart.remove_item(product, quantity)
            print(f"\nRemoved {quantity} {product.name}(s) from cart\n")
        except (ValueError, IndexError):
            print("\nError: Invalid selection. Please enter a valid item number and quantity.\n")

    def checkout(self):
        """Process payment and generate receipt"""

        if not self.cart.items:
            print("Your cart is empty")
            return
        while True:
            subtotal = self.cart.calculate_subtotal()
            discount = subtotal * 0.05 if subtotal > 5000 else 0
            tax = (subtotal - discount) * 0.10
            total = subtotal - discount + tax


        # Display order summary
            print("\n****************************** ORDER SUMMARY ******************************\n")
            self.cart.view_cart()

            if discount > 0:
                print("")
            print(f"DISCOUNT (5%): -${discount:.2f}")
            print(f"TAX (10%): ${tax:.2f}")
            print(f"TOTAL: ${total:.2f}")

        #Prompt the user to add more items
            print("\nPlease select an option below to add or remove items from your cart. Select 3 to proceed to checkout")
            print("1. Add an Item to your cart")
            print("2. Remove an Item from your cart")
            print("3. No, Please proceed to payment")
            choice = input("Enter choice (1-3): ")

            if choice == "1":
                self.add_to_cart()
            elif choice == "2":
             self.remove_from_cart()
            elif choice == "3":
             break
            else:
             print("Invalid choice. Please enter 1-3")
             continue

      # Process payment
        while True:
            try:
                print("")
                amount = float(input("Enter payment amount: $"))
                print("")
                if amount < total:
                    print(f"Amount must be at least ${total:.2f}")
                    continue

                change = amount - total
                self.generate_receipt(subtotal, discount, tax, total, amount, change)

                # Update stock levels after receipt is generated
                for product, quantity in self.cart.items.items():
                    product.update_stock(quantity)

                self.cart = ShoppingCart()  # Reset cart
                break

            except ValueError:
                print("Invalid amount. Please enter a number")

    def generate_receipt(self, subtotal, discount, tax, total, amount, change):
        """Print formatted receipt"""
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("*********************************** RECEIPT ***********************************")
        print("BestBuy Food, Beverages, and Household Items Retail Store". center(80))
        print("16 East Street, St. James, Contact: (876) 940-2025". center(80))
        print(f"Date: {now}". center(80))
        print("*" * 80)
        print("{:<25} {:<12} {:<12} {:<12}".format("Product", "Price", "Qty", "Total"))

        for product, quantity in self.cart.items.items(): # This block of code is responsible for the products purchased to be displayed on the receipt
         print(f"{product.name:<25} ${product.price:<11.2f} {quantity:<12} ${product.price * quantity:11.2f}") # This is the format at which the products are displayed.

        print("*" * 80)
        print(f"SUBTOTAL: ${subtotal:.2f}")
        if discount > 0:
            print(f"DISCOUNT: -${discount:.2f}")
        print(f"TAX: ${tax:.2f}")
        print(f"TOTAL: ${total:.2f}")
        print(f"PAID: ${amount:.2f}")
        print(f"CHANGE: ${change:.2f}")
        print("\nThank you for shopping with us!\n")
        print("*" * 80)

        # Check low stock
    def show_low_stock_alerts(self):
        low_stock = [p for p in self.products if p.stock < 5] #If product name and product stock is less than 5 print low stock alert and include the stock remaining.
        if low_stock:
            print("ALERT: Low stock items:". center(80))
            print("")
            for product in low_stock:
                print(f" {product.name}: {product.stock} remaining". center(80))

    def run(self):
        """Main program loop"""
        while True:
            print("\n********************** BESTBUY POINT OF SALE SYSTEM MENU ***********************\n")
            self.show_low_stock_alerts()  # Show alerts after purchase
            print("")
            print("*" * 80)
            print("1. View Products")
            print("2. Add to Cart")
            print("3. Remove from Cart")
            print("4. View Cart")
            print("5. Checkout")
            print("6. Exit")
            print("*" * 80)
            choice = input("Enter choice (1-6): ")
            print("*" * 80)

            if choice == "1":
                self.display_products()
            elif choice == "2":
                self.add_to_cart()
            elif choice == "3":
                self.remove_from_cart()
            elif choice == "4":
                self.cart.view_cart()
            elif choice == "5":
                self.checkout()
                self.cart = ShoppingCart()  # Reset cart after checkout
            elif choice == "6":
                print("THANK YOU FOR USING BESTBUY POINT OF SALE SYSTEM!")
                break
            else:
                print("Opps! Invalid choice or input. Please try again with a valid choice 1-6!")

# Run the POS system
if __name__ == "__main__":
    pos = POSSystem()
    pos.run()
