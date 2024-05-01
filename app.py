from flask import Flask, render_template
from web3 import Web3
from solcx import compile_source
import json

app = Flask(__name__)

# Install Solidity Compiler (solc) if not installed
solcx.install_solc('0.8.7')
print("Solidity compiler (solc) installed successfully.")

# Connect to the Ethereum mainnet using Infura
infura_url = "https://mainnet.infura.io/v3/204b2e25317d4e3c8d59bf61d1830702"  # Replace with your Infura API key

# Account's private key
private_key = "YOUR_PRIVATE_KEY"

# Compile Solidity source code
with open("./RetailCoin.sol", "r") as file:
    source_code = file.read()

compiled_code = compile_source(source_code)
contract_interface = compiled_code["<stdin>:RetailCoin"]

# Connect to the Ethereum network
w3 = Web3(Web3.HTTPProvider(infura_url))

# Set default account
w3.eth.defaultAccount = w3.eth.account.privateKeyToAccount(private_key).address

# Deploy the contract
RetailCoin = w3.eth.contract(
    abi=contract_interface["abi"],
    bytecode=contract_interface["bin"]
)
tx_hash = RetailCoin.constructor().transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

contract_address = tx_receipt.contractAddress

# Interact with the contract
contract_instance = w3.eth.contract(
    address=contract_address,
    abi=contract_interface["abi"]
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/totalSupply")
def total_supply():
    total_supply = contract_instance.functions.totalSupply().call()
    return f"Total Supply: {total_supply}"

if __name__ == "__main__":
    app.run(debug=True)
