from flask import Flask, jsonify, request
from webthree import webthree, HTTPProvider
from solcx import compile_source

app = Flask(__name__)

# Connect to the local Ethereum network
webthree = webthree(HTTPProvider("http://localhost:8545"))

# Check if the connection Ethreum is successful
if webthree.isConnected():
    print("Connected to Ethereum network!")
else:
    print("Failed to connect to Ethereum network.")

# Compile the Solidity contract
contract_source_code = open("TestCoin.sol", "r").read()
compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol["<stdin>:TestCoin"]
abi = contract_interface["abi"]
bytecode = contract_interface["bin"]

# Deploy the contract
total_supply = 1000
contract = webthree.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = contract.constructor(total_supply).transact()
tx_receipt = webthree.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt["contractAddress"]

# Create a new contract instance
contract = webthree.eth.contract(address=contract_address, abi=abi)

# Define a route to get the total supply
@app.route("/total_supply")
def total_supply():
    total_supply = contract.functions.totalSupply().call()
    return jsonify({"total_supply": total_supply})

# Define a route to get the balance of an address
@app.route("/balance/<address>")
def balance(address):
    balance = contract.functions.balanceOf(address).call()
    return jsonify({"balance": balance})

# Define a route to send TestCoins to an address
@app.route("/send", methods=["POST"])
def send():
    from_address = webthree.eth.defaultAccount
    to_address = request.form["to"]
    value = int(request.form["value"])

    # Send the transaction
    tx_hash = contract.functions.transfer(to_address, value).transact({"from": from_address})
    tx_receipt = webthree.eth.wait_for_transaction_receipt(tx_hash)

    # Return the transaction hash
    return jsonify({"tx_hash": tx_hash.hex()})

if __name__ == "__main__":
    app.run(debug=True)
