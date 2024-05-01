from flask import Flask, jsonify, request
from web3 import Web3, HTTPProvider
from solcx import compile_source, install_solc

app = Flask(__name__)

try:
    # Install Solidity Compiler (solc) if not installed
    install_solc()
    print("Solidity compiler (solc) installed successfully.")
except Exception as e:
    print(f"Failed to install Solidity compiler (solc): {e}")
    exit()

# Connect to the Ethereum mainnet using Infura
infura_url = "https://mainnet.infura.io/v3/204b2e25317d4e3c8d59bf61d1830702"  # Ganti YOUR_API_KEY dengan kunci API Infura Anda
web3 = Web3(HTTPProvider(infura_url))

try:
    # Check if the connection to Ethereum is successful
    network_version = web3.net.version
    print(f"Connected to Ethereum network with Version: {network_version}")
    accounts = web3.eth.accounts
    if accounts:
        default_account = accounts[0]
        print(f"Default account: {default_account}")
    else:
        print("No accounts found.")
except Exception as e:
    print(f"Failed to connect to Ethereum network: {e}")
    exit()

# Compile the Solidity contract
contract_source_code = open("RetailCoin.sol", "r").read()
compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol["<stdin>:TestCoin"]
abi = contract_interface["abi"]
bytecode = contract_interface["bin"]

# Define a route to deploy the contract
@app.route("/deploy", methods=["GET"])
def deploy():
    # Get the nonce for the default account
    nonce = web3.eth.getTransactionCount(default_account)

    # Deploy the contract
    contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor(1000).buildTransaction({
        "from": default_account,
        "nonce": nonce,
        "gas": 1000000,
        "gasPrice": web3.toWei("10", "gwei")
    })

    # Sign the transaction with MetaMask and Infura
    # This part needs to be done manually by the user using MetaMask
    # and then submitted through a separate application
    # as Flask cannot interact directly with MetaMask
    # You will need to provide instructions for users to interact with MetaMask
    # and submit the signed transaction to this endpoint
    # For demonstration purposes, I'll leave this part as a placeholder
    # and you need to replace it with the actual implementation.
    signed_tx = "SIGNED_TRANSACTION_FROM_METAMASK"

    tx_hash = web3.eth.sendRawTransaction(signed_tx)

    # Wait for the transaction to be mined and confirmed
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    contract_address = tx_receipt["contractAddress"]

    # Return the contract address
    return jsonify({"contractAddress": contract_address})

if __name__ == "__main__":
    app.run(debug=True)
