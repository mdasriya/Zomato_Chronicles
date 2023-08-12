import pickle

class Dish:
    def __init__(self, dish_id, name, price, available):
        self.dish_id = dish_id
        self.name = name
        self.price = price
        self.available = available

class Order:
    def __init__(self, order_id, customer_name, dish_ids):
        self.order_id = order_id
        self.customer_name = customer_name
        self.dish_ids = dish_ids
        self.status = 'received'

class ZomatoSystem:
    def __init__(self):
        self.menu = {}
        self.orders = {}
        self.order_counter = 1

    def add_dish(self, dish_id, name, price, available):
        dish = Dish(dish_id, name, price, available)
        self.menu[dish_id] = dish

    def remove_dish(self, dish_id):
        if dish_id in self.menu:
            del self.menu[dish_id]
            for order in self.orders.values():
                if dish_id in order.dish_ids:
                    order.dish_ids.remove(dish_id)

    def update_dish_availability(self, dish_id, available):
        if dish_id in self.menu:
            self.menu[dish_id].available = available

    def take_order(self, customer_name, dish_ids):
        for dish_id in dish_ids:
            if dish_id not in self.menu or not self.menu[dish_id].available:
                print(f"Error: Dish {dish_id} is not available.")
                return
        order = Order(self.order_counter, customer_name, dish_ids)
        self.orders[self.order_counter] = order
        self.order_counter += 1

    def update_order_status(self, order_id, new_status):
        if order_id in self.orders:
            self.orders[order_id].status = new_status
        else:
            print("Error: Invalid order ID.")

    def review_orders(self, status_filter=None):
        for order in self.orders.values():
            if status_filter is None or order.status == status_filter:
                print(f"Order ID: {order.order_id}, Customer: {order.customer_name}, Status: {order.status}")

    def calculate_order_total(self, order_id):
        if order_id in self.orders:
            total_price = sum(self.menu[dish_id].price for dish_id in self.orders[order_id].dish_ids)
            return total_price
        else:
            return None

    def save_data(self, filename):
        with open(filename, 'wb') as f:
            data = {'menu': self.menu, 'orders': self.orders, 'order_counter': self.order_counter}
            pickle.dump(data, f)

    def load_data(self, filename):
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                self.menu = data['menu']
                self.orders = data['orders']
                self.order_counter = data['order_counter']
        except FileNotFoundError:
            pass

    def run(self):
        self.load_data('zomato_data.pkl')

        while True:
            print("\nWelcome to Zesty Zomato")
            print("1. Add Dish")
            print("2. Remove Dish")
            print("3. Update Dish Availability")
            print("4. Take Order")
            print("5. Update Order Status")
            print("6. Review Orders")
            print("7. Calculate Order Total Price")
            print("8. Save and Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                dish_id = input("Enter Dish ID: ")
                name = input("Enter Dish Name: ")
                price = float(input("Enter Price: "))
                available = input("Is Dish Available? (yes/no): ").lower() == 'yes'
                self.add_dish(dish_id, name, price, available)
                print("new Dish is added")

            elif choice == '2':
                dish_id = input("Enter Dish ID to remove: ")
                self.remove_dish(dish_id)

            elif choice == '3':
                dish_id = input("Enter Dish ID to update availability: ")
                available = input("Is Dish Available? (yes/no): ").lower() == 'yes'
                self.update_dish_availability(dish_id, available)

            elif choice == '4':
                customer_name = input("Enter Customer Name: ")
                dish_ids = input("Enter Dish IDs (comma-separated): ").split(',')
                dish_ids = [dish_id.strip() for dish_id in dish_ids]
                self.take_order(customer_name, dish_ids)

            elif choice == '5':
                order_id = int(input("Enter Order ID: "))
                new_status = input("Enter New Status: ")
                self.update_order_status(order_id, new_status)

            elif choice == '6':
                status_filter = input("Enter status to filter (press Enter to skip): ")
                self.review_orders(status_filter)

            elif choice == '7':
                order_id = int(input("Enter Order ID: "))
                total_price = self.calculate_order_total(order_id)
                if total_price is not None:
                    print(f"Total Price for Order ID {order_id}: ${total_price:.2f}")
                else:
                    print("Invalid order ID.")

            elif choice == '8':
                self.save_data('zomato_data.pkl')
                print("Data saved. Exiting Zesty Zomato. Have a great day!")
                break

            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    zomato_system = ZomatoSystem()
    zomato_system.run()
