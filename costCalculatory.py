try:
    tickets=int(input("Enter your number of tickets: "))
    boxes = int(tickets / 50)
    print(f"You will be able to mint {boxes} boxes")
    gas_fees = float(input("Target for gas in GWEI: "))
    gas_usage = 75000 #slightly pessimistic estimate
    minting_cost = gas_fees * gas_usage * boxes / 1000000000
    print(f"To mint {boxes} at {gas_fees} you will need to pay about {minting_cost} ETH")
except ValueError:
    print("Error: Invalid number")

input("Press Enter to exit ...")