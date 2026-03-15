import os
import sys
import time

# PATH FIX
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import kitchen_manager

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_kds():
    while True:
        clear_screen()
        print("👨‍🍳 " + "="*65)
        print("           KITCHEN DISPLAY SYSTEM (KDS) - LIVE QUEUE")
        print("="*65)
        print(f"{'ID':<6} {'Customer':<12} {'Status':<12} {'Order Details'}")
        print("-" * 65)
        
        queue = kitchen_manager.get_active_queue()
        
        if not queue:
            print("\n           ✨ No pending orders. Kitchen is clear! ✨")
        else:
            for order in queue:
                status_color = order['status'].upper()
                print(f"#{order['order_id']:<5} {order['username']:<12} {status_color:<12} {order['items']}")
        
        print("\n" + "="*65)
        print("ACTIONS: [s] Start Preparing | [r] Mark Ready | [c] Complete | [u] Update List")
        print("Type 'exit' to close.")
        
        choice = input("\nSelect Action (e.g., 's 101'): ").lower().split()
        
        if not choice: continue
        
        cmd = choice[0]
        
        if cmd == 'exit': break
        if cmd == 'u': continue # Just refreshes the loop
        
        if len(choice) < 2:
            print("❌ Please provide Order ID (e.g., 's 105')")
            time.sleep(1)
            continue
            
        oid = choice[1]
        
        if cmd == 's':
            kitchen_manager.update_order_status(oid, 'preparing')
        elif cmd == 'r':
            kitchen_manager.update_order_status(oid, 'ready')
        elif cmd == 'c':
            kitchen_manager.update_order_status(oid, 'completed')
        else:
            print("❌ Unknown Command.")
            time.sleep(1)

if __name__ == "__main__":
    display_kds()