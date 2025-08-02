from ib_insync import *

def main():
    print("[LOG] IBKRAPI_test01 has started.")
    # Connect to TWS or IB Gateway (must be running in Paper Trading mode)
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)  # Port 7497 is for Paper Trading by default

    # Print account summary
    account_summary = ib.accountSummary()
    print("Account Summary:")
    for item in account_summary:
        print(f"{item.tag}: {item.value} {item.currency}")

    # Optional: Get current positions (should be empty if fresh account)
    positions = ib.positions()
    print("\nOpen Positions:")
    for pos in positions:   
        print(pos)

    # Disconnect after done
    ib.disconnect()

if __name__ == "__main__":
    main()
