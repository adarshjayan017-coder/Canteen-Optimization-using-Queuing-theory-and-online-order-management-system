import os
import sys

# PATH FIX
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Student_app.modules import menu_manager
from core import auth_handler

def admin_login():
    """
    The Gatekeeper: Handles authentication and role-checking.
    Returns True if Admin is verified, False otherwise.
    """
    print("\n" + "🔐 " + "="*35)
    print("      CANTEEN ADMIN SYSTEM")
    print("="*35)
    uname = input("Admin Username: ")
    pwd = input("Admin Password: ")
    
    user = auth_handler.login_user(uname, pwd)
    
    # "ONE-WAY STREET" SECURITY: Only Admin role can enter here
    if user and user['role'] == 'admin':
        print(f"✅ Access Granted. Welcome, Admin {user['username']}.")
        return True
    elif user:
        print("❌ ACCESS DENIED: Students cannot access this portal.")
        return False
    else:
        print("❌ Login Failed: Invalid credentials.")
        return False

def admin_menu():
    """
    The Protected Management Zone.
    """
    while True:
        print("\n" + "🛠️ " + "="*48)
        print("      🏪 CANTEEN SYSTEM: MENU MANAGEMENT")
        print("="*48)
        print("1. View Menu (All Items)")
        print("2. Add New Menu Item")
        print("3. Edit Item (Name/Price/Status)")
        print("4. Quick Stock-Out / In-Stock Toggle")
        print("0. Logout & Exit")
        print("-" * 50)
        
        choice = input("Select an option: ")

        if choice == '1':
            menu = menu_manager.get_full_menu()
            print("\n" + "-"*65)
            print(f"{'ID':<5} {'Name':<20} {'Price':<8} {'Status':<15}")
            print("-" * 65)
            for m in menu:
                if m['is_available'] == 1: status = "Active"
                elif m['is_available'] == 0: status = "STOCK OUT"
                else: status = "INACTIVE (Hidden)"
                
                print(f"{m['item_id']:<5} {m['item_name']:<20} ₹{m['price']:<7} {status:<15}")

        elif choice == '2':
            try:
                name = input("Enter Item Name: ")
                price = float(input("Enter Price (₹): "))
                cat = input("Enter Category: ")
                menu_manager.add_menu_item(name, price, cat)
            except ValueError:
                print("❌ Error: Price must be a number.")

        elif choice == '3':
            try:
                iid = input("Enter Item ID to edit: ")
                if not iid.isdigit(): continue
                
                print("\n(Leave blank to keep current value)")
                name = input("New Name: ")
                
                p_input = input("New Price: ")
                price = float(p_input) if p_input.strip() else None
                
                cat = input("New Category: ")
                
                print("Change Status? (1: Active, 0: Stock Out, -1: Inactive, Enter: Skip)")
                s_input = input("New Status: ")
                status = int(s_input) if s_input.strip() in ['1', '0', '-1'] else None
                
                menu_manager.alter_menu_item(iid, name, price, cat, status)
            except ValueError:
                print("❌ Error: Invalid numeric input.")

        elif choice == '4':
            iid = input("Enter Item ID: ")
            if iid.isdigit():
                print("1. Set to In Stock\n2. Set to Stock Out\n3. Set to Inactive")
                st_choice = input("Select (1/2/3): ")
                mapping = {'1': 1, '2': 0, '3': -1}
                if st_choice in mapping:
                    menu_manager.toggle_availability(iid, mapping[st_choice])
                else:
                    print("❌ Invalid selection.")

        elif choice == '0':
            print("Logging out... Goodbye!")
            break

if __name__ == "__main__":
    # First, authenticate the user
    if admin_login():
        # If successful, open the menu management
        admin_menu()
    else:
        print("Application closing due to unauthorized access.")