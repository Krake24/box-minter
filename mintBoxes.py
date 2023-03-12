import pandas as pd
import time
import json
import os
from web3 import Web3
from getpass import getpass

def clear():
    print("\033[H\033[J", end="")

w3 = Web3(Web3.HTTPProvider("https://cloudflare-eth.com/v1/mainnet"))

CONTRACT_ADDRESS = Web3.toChecksumAddress('0xb3cE7c6abF0801de81437cB94C1c8c84eA54346c')
abi = '[{"inputs":[{"internalType":"address","name":"_nftAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"CAIGVoucheredMinted","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DEPLOYER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"VOUCHER_SIGNER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct CAIGVoucheredMintingFactory.Voucher","name":"voucher","type":"tuple"}],"name":"digestVoucher","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"nftAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"components":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct CAIGVoucheredMintingFactory.Voucher","name":"_voucher","type":"tuple"}],"name":"redeem","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"selfDestruct","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct CAIGVoucheredMintingFactory.Voucher","name":"voucher","type":"tuple"}],"name":"verify","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

print("This program will help you mint all of your boxes. Please make sure to understand your options. If you have any questions please contact Pirre.")
print("At any point you will be able to abort the exexution of this program by pressing CTRL+C, unless you have already started blockchain transactions.")
print("Before any blockchain transactions will happen however, you will be prompted, if you really want to move continue.")
input("Press Enter to start")
clear()

try:
    data = json.loads(open(os.path.dirname(os.path.realpath(__file__))+"/tickets.json", "r").read())
    boxes = data['unredeemedNftVouchers']

    print("What is the highest gas fee you want to pay?")
    max_fees = float(input("Max gas fees: "))
    clear()

    print("Please enter the private key for the wallet you want to mint from:")
    private_key = getpass("Private Key:")
    clear()

    address = w3.eth.account.from_key(private_key).address
    balance = w3.eth.getBalance(address) / 1000000000000000000
    print(f"Your wallet {address} has a balance of: {balance}")

    box_number = len(boxes)
    number_to_mint = box_number

    costs_to_mint_one = 75 * max_fees / 1000000 
    gas_fees = box_number * costs_to_mint_one
    print(f"You have {box_number} boxes to mint. At a gas fee of {max_fees}, you will require about {gas_fees} ETH to mint all of these boxes.")
    
    if balance < gas_fees:
        number_to_mint = int(balance / costs_to_mint_one)
        print(f"You have enough tickets to mint {box_number} of boxes, but your current balance only allows to mint {number_to_mint} at {max_fees} GWEI")

    print(f"How many boxes do you want to mint? (Press enter to mint the maximum of {number_to_mint})")
    number_to_mint=int(input(f"Boxes to mint (default: {number_to_mint})") or number_to_mint)
    gas_fees = number_to_mint * costs_to_mint_one
    clear()

    options=[]
    options.append("") #dummy to match index with mode chosen
    options.append("1. Safe, but slowest: Mint one by one only when gas is lower than the threshold")
    options.append("2. Pretty safe & quick: Mint all at once, but wait for gas to be lower than the threshold")
    options.append("3. Risky, but quick: Mint all at once, but wait for gas to be lower than the threshold")

    print("Please choose an option:")
    print(options[1])
    print(options[2])
    print(options[3])
    print("For options 1 & 2, you need to leave this window open, until the program finishes")
    print("Depending on gas threshold the options 2 & 3 might leave your minting wallet with a lot of stuck transactions.")
    mode = int(input("option: "))
    clear()

    if mode > 3 or mode < 1:
        raise Exception("Invalid option")

    print("Choose a wallet that will receive the boxes minted:")
    recipient = Web3.toChecksumAddress(input("recipient address: "))
    clear()

    print("===== Summary =====")
    print(f"Minting wallet: {address}")
    print(f"Recipient wallet: {recipient}")
    print(f"Available funds: {balance}")
    print(f"Required funds estimate: {gas_fees}")
    print(f"Number of boxes to be minted: {number_to_mint}")
    print(f"Max gas fees: {max_fees}")
    print(f"Mode: {options[mode]}")
    print("===================")
    print()
    print("Please make sure to check the summary and be sure that you want to proceed. As a reminder, you can ask Pirre, should you have any questions.")
    print("The minting process will be started now. If you are certain you want to proceed, please type START (all upper case). In any other case this program will exit.")
    if max_fees < 15:
        print()
        print(f"WARNING: {max_fees} is a really low value for gas price. Please make sure, that your are certain you want to use this value")
    confirmation=input("Type START to begin: ")
    clear()
    if not confirmation == "START":
        raise Exception("Program aborted")
    
    contract = w3.eth.contract(
        address=CONTRACT_ADDRESS,
        abi=abi,
    )
    
    nonce = w3.eth.get_transaction_count(address)
    for index in range(0,number_to_mint):
        box = boxes[index]
        gas_fees=w3.eth.gas_price / 1000000000 + 1 # adding one GWEI to current gas, since this number is base gas
        while (mode < 3 and gas_fees > max_fees):
            print(f"Waiting for gas to become lower than {max_fees}, currently: {gas_fees}")
            clear()            
            time.sleep(int(gas_fees - max_fees))
            gas_fees=w3.eth.gas_price / 1000000000

        token = int(box['tokenId'],16)
        signature = box['signature']

        fun = contract.functions.redeem(recipient, (token, signature))

        tx_data = fun.build_transaction(
            {
                'from' : address,
                'nonce' : nonce,
            }
        )

        # ## ONLY FOR SETTING MANUAL GAS
        tx_data['maxFeePerGas'] = int(max_fees * 1000000000)
        tx_create = w3.eth.account.sign_transaction(tx_data, private_key)

        tx_hash = w3.eth.send_raw_transaction(tx_create.rawTransaction)
        print(f'Transaction created: https://etherscan.io/tx/{tx_hash.hex()}')

        if mode == 1:
            print("Waiting for transaction to be completed")
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=24 * 60 * 60)
            print(f'Transaction successful')

        nonce=nonce + 1

except Exception as e:
    print(f"{str(e)}")

input("Press Enter to exit ...")