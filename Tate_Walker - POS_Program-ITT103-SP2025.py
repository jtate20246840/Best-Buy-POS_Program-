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
        print("")
        print("********************************* BESTBUY SHOPPING CART *********************************")
        print("")
        print("{:<20} {:<10} {:<10} {:<10}".format("Product", "Price", "Qty", "Total"))
        for product, quantity in self.items.items():
            print(f"{product.name:<20} ${product.price:<9.2f} {quantity:<10} ${product.price * quantity:<9.2f}")

        print("*" * 80)
        print(f"SUBTOTAL: ${self.calculate_subtotal():.2f}")


class POSSystem:
    def __init__(self):
        self.products = self.initialize_products()
        self.cart = ShoppingCart()

    @classmethod
    def initialize_products(cls):
        """Create initial product catalog"""
        return [
            Product("Gain Laundry Detergent", 200, 10),
            Product("Paper Towels Bundle", 500, 15),
            Product("Tissues - Pack of 24", 150, 20),
            Product("Trash Bags", 100, 10),
            Product("Zip Bags", 50, 25),
            Product("Special K Cereal Chocolate", 300, 16),
            Product("Exotic Spices Bundle", 400, 3),
            Product("Moscato Wine", 250, 5),
            Product("Fresh Product Combo", 120, 12),
            Product("Exotic Breakfast Combo", 290, 4)]

    def display_products(self):
        """Show available products"""
        print("")
        print("******************************** BESTBUY PRODUCT CATALOG *******************************")
        print("")
        for idx, product in enumerate(self.products, 1): # The enumerate function and the idx (index) variable works together to create a numbered product menu for a smooth user selection.
            stock_alert = " (LOW STOCK!)" if product.stock < 5 else ""
            print(f"{idx}. {product}{stock_alert}")

    def add_to_cart(self):
        """Add selected product to cart"""
        self.display_products()
        try:
            print("")
            choice = int(input("Enter product number: ")) - 1
            print("")
            if not 0 <= choice < len(self.products):
                raise ValueError("Invalid product number")

            product = self.products[choice]
            quantity = int(input(f"Enter quantity for {product.name}: "))

            self.cart.add_item(product, quantity)
            print(f"Added {quantity} {product.name}(s) to cart")

        except (ValueError, IndexError):
            print("Error: Invalid product selection")

    def remove_from_cart(self):
        """Remove item from cart"""
        self.cart.view_cart()
        if not self.cart.items:
            return

        try:
            print("")
            product_name = input("Enter product name to remove: ")
            print("")
            product = next((p for p in self.cart.items.keys() if p.name.lower() == product_name.lower()), None)

            if not product:
                raise ValueError("Product not found in cart")

            quantity = int(input(f"Enter quantity to remove (max {self.cart.items[product]}): "))
            self.cart.remove_item(product, quantity)
            print(f"Removed {quantity} {product.name}(s) from cart")

        except ValueError:
            print("Error: Invalid Product Name or Quantity Amount")
            print("The product name is case sensitive and has to be entered exactly how it is shown in the cart. Upper & Lower case letters respectively.")

    def checkout(self):
        """Process payment and generate receipt"""
        if not self.cart.items:
            print("Your cart is empty")
            return

        subtotal = self.cart.calculate_subtotal()
        discount = subtotal * 0.05 if subtotal > 5000 else 0
        tax = (subtotal - discount) * 0.10
        total = subtotal - discount + tax

        # Display order summary
        print("")
        print("****************************** ORDER SUMMARY ******************************")
        print("")
        self.cart.view_cart()

        if discount > 0:
            print(f"DISCOUNT (5%): -${discount:.2f}")
        print(f"TAX (10%): ${tax:.2f}")
        print(f"TOTAL: ${total:.2f}")

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

                # Update stock levels
                for product, quantity in self.cart.items.items():
                    product.update_stock(quantity)

                self.cart = ShoppingCart()  # Reset cart
                break

            except ValueError:
                print("Invalid amount. Please enter a number")

    def generate_receipt(self, subtotal, discount, tax, total, amount, change):
        """Print formatted receipt"""
        print("")
        print("************************** BESTBUY POINT OF SALE SYSTEM MENU **************************")
        print("*********************************** RECEIPT ***********************************")
        print("")
        print("BestBuy groceries, beverages, and household items Retail Store")
        print("16 East Street, St. James, Contact: (876) 940-2025")
        print("*" * 80)
        print("{:<20} {:<10} {:<10} {:<10}".format("Product", "Price", "Qty", "Total"))

        for product, quantity in self.cart.items.items(): product.update_stock(quantity) #This block of code demonstrates the updated product quantity in the low stock alert
        print(f"{product.name:<20} ${product.price:<9.2f} {quantity:<10} ${product.price * quantity:<9.2f}")

        print("*" * 80)
        print(f"SUBTOTAL: ${subtotal:.2f}")
        if discount > 0:
            print(f"DISCOUNT: -${discount:.2f}")
        print(f"TAX: ${tax:.2f}")
        print(f"TOTAL: ${total:.2f}")
        print(f"PAID: ${amount:.2f}")
        print(f"CHANGE: ${change:.2f}")
        print("")
        print("Thank you for shopping with us!")
        print("")
        print("*" * 80)

        # Check low stock
        low_stock = [p for p in self.products if p.stock < 5] #If product name and product stock is less than 5 print low stock alert and include the stock remaining.
        if low_stock:
            print("")
            print("ALERT: Low stock items:")
            print("")
            for product in low_stock:
                print(f"- {product.name}: {product.stock} remaining")

    def run(self):
        """Main program loop"""
        while True:
            print("")
            print("************************** BESTBUY POINT OF SALE SYSTEM MENU ***************************")
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
            elif choice == "6":
                print("THANK YOU FOR USING BESTBUY POINT OF SALE SYSTEM!")
                break
            else:
                print("Opps! Invalid choice or input. Please try again!")


# Run the POS system
if __name__ == "__main__":
    pos = POSSystem()
    pos.run()