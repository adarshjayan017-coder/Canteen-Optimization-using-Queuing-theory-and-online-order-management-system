import os
import sys
from datetime import datetime

# PATH FIX: Ensures this script can "see" the core and modules folders
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import auth_handler
from modules import student_manager

def clear_screen():
    # Clears the terminal for a cleaner User Experience (UX)
    os.system('cls' if os.name == 'nt' else 'clear')

def display_history(user_id):
    """Option 3: Displays past orders and their current lifecycle status."""
    clear_screen()
    print("\n" + "📜 " + "="*60)
    print(f"{'Order ID':<10} {'Date':<12} {'Total':<10} {'Status':<12}")
    print("="*60)
    
    history = student_manager.get_user_order_history(user_id)
    
    if not history:
        print("   No previous orders found. Time to grab a snack!")
    else:
        for order in history:
            # Format the DB timestamp for better readability
            date_str = order['created_at'].strftime("%Y-%m-%d")
            status_display = order['status'].upper()
            
            print(f"#{order['order_id']:<9} {date_str:<12} ₹{order['total_amount']:<9} {status_display:<12}")
            print(f"   Items: {order['items_list']}")
            print("-" * 60)
    
    input("\nPress Enter to return to main menu...")

def student_portal(user_data):
    """The main dashboard where Demand (Orders) is created."""
    # Now using a list of Dictionaries for better data handling
    cart = [] 
    
    while True:
        clear_screen()
        print(f"🏠 WELCOME TO THE CANTEEN, {user_data['username'].upper()}!")
        print(f"User ID: {user_data['user_id']} | Access: {user_data['role'].capitalize()}")
        print("="*45)
        print("1. 🍴 Browse Menu & Add to Cart")
        print("2. 🛒 View Cart & Place Order")
        print("3. 📜 My Order History")
        print("0. 🚪 Logout")
        print("-" * 45)
        
        choice = input("Select an option: ")

        if choice == '1':
            menu = student_manager.get_available_menu()
            print("\n--- TODAY'S MENU ---")
            print(f"{'ID':<5} {'Item Name':<20} {'Price':<10}")
            print("-" * 35)
            for m in menu:
                print(f"[{m['item_id']}] {m['item_name']:<20} ₹{m['price']}")
            
            iid = input("\nEnter Item ID to add (or 'b' to go back): ")
            if iid.lower() != 'b' and iid.isdigit():
                item = next((x for x in menu if x['item_id'] == int(iid)), None)
                if item:
                    try:
                        qty = int(input(f"Quantity for {item['item_name']}: "))
                        if qty > 0:
                            # Added as a dictionary for UI compatibility
                            cart.append({
                                'item_id': item['item_id'], 
                                'qty': qty, 
                                'price': item['price'], 
                                'name': item['item_name']
                            })
                            print(f"✅ Added to cart.")
                        else:
                            print("❌ Quantity must be positive.")
                    except ValueError:
                        print("❌ Please enter a valid number.")
                else:
                    print("❌ Item not found.")
                input("\nPress Enter...")

        elif choice == '2':
            if not cart:
                print("\n🛒 Your cart is empty!")
                input("Press Enter...")
                continue
            
            clear_screen()
            print("--- YOUR CURRENT CART ---")
            total = 0
            for item in cart:
                subtotal = item['qty'] * item['price']
                total += subtotal
                print(f"• {item['name']} (x{item['qty']}) = ₹{subtotal}")
            
            print("-" * 30)
            print(f"TOTAL PAYABLE: ₹{total}")
            print("-" * 30)
            
            confirm = input("\nConfirm Order? (y/n): ")
            if confirm.lower() == 'y':
                # Pass the list of dictionaries directly to the manager
                success, result = student_manager.place_order(user_data['user_id'], cart)
                
                if success:
                    print(f"\n🎉 Order #{result} placed successfully!")
                    cart = [] # Clear cart after success
                else:
                    print(f"\n❌ Order Failed: {result}")
                input("\nPress Enter...")

        elif choice == '3':
            display_history(user_data['user_id'])

        elif choice == '0':
            print("Logging out...")
            break

def main():
    """Gatekeeper: Entry point for the User App."""
    while True:
        clear_screen()
        print("========================================")
        print("     🎓 CANTEEN DIGITAL TERMINAL")
        print("========================================")
        print("1. Login")
        print("2. Register New Account")
        print("0. Exit")
        entry = input("\nChoice: ")

        if entry == '1':
            uname = input("Username: ")
            pwd = input("Password: ")
            user = auth_handler.login_user(uname, pwd)
            
            if user:
                # Security: Both students and admins can use this portal
                student_portal(user)
            else:
                input("\nInvalid Login. Press Enter to try again...")

        elif entry == '2':
            print("\n--- NEW STUDENT REGISTRATION ---")
            u = input("Username: ")
            e = input("Email: ")
            p = input("Password: ")
            success, msg = auth_handler.register_user(u, e, p, role='student')
            print(f"{'✅' if success else '❌'} {msg}")
            input("Press Enter...")

        elif entry == '0':
            break

if __name__ == "__main__":
    main()