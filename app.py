from flask import Flask, jsonify, request
from web3 import Web3, HTTPProvider
from solcx import compile_source

app = Flask(__name__)

# Connect to the Ropsten test network using Infura
webthree = Web3(HTTPProvider("Your Main Net Infura ETH ID URL HTTPS"))

try:
    # Check if the connection to Ethereum is successful
    network_id = webthree.eth.net.get_id()
    print(f"Connected to Ethereum network with ID: {network_id}")
    accounts = webthree.eth.accounts
    if accounts:
        default_account = accounts[0]
        print(f"Default account: {default_account}")
    else:
        print("No accounts found.")
except Exception as e:
    print(f"Failed to connect to Ethereum network: {e}")

# Compile the Solidity contract
contract_source_code = open("TestCoin.sol", "r").read()
compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol["<stdin>:TestCoin"]
abi = contract_interface["abi"]
bytecode = contract_interface["bin"]

# Define a route to deploy the contract
@app.route("/deploy", methods=["GET"])
def deploy():
    # Get the nonce for the default account
    nonce = webthree.eth.getTransactionCount(default_account)

    # Deploy the contract
    contract = webthree.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor(1000).buildTransaction({
        "from": default_account,
        "nonce": nonce,
        "gas": 1000000,
        "gasPrice": webthree.toWei("10", "gwei")
    })
    signed_tx = webthree.eth.account.signTransaction(tx_hash, private_key=YOUR_PRIVATE_KEY)
    tx_hash = webthree.eth.sendRawTransaction(signed_tx.rawTransaction)

    # Wait for the transaction to be mined and confirmed
    tx_receipt = webthree.eth.waitForTransactionReceipt(tx_hash)
    contract_address = tx_receipt["contractAddress"]

    # Return the contract address
    return jsonify({"contractAddress": contract_address})

if __name__ == "__main__":
    app.run(debug=True)
