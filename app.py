from flask import Flask, jsonify, request
from web3 import Web3, HTTPProvider
from solcx import compile_standard

app = Flask(_name_)

# Connected Blockchain Node Ethreum Contract
webthree = Web3(HTTPProvider("http://localhost:8545"))

# Compile Solidity contract
contract_source_code = '''
pragma solidity ^0.8.0;

contract TestCoin {
    string public name = "TestCoin";
    string public symbol = "TSC";
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(uint256 initialSupply) {
        totalSupply = initialSupply;
        balanceOf[msg.sender] = initialSupply;
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        require(balanceOf[_to] + _value >= balanceOf[_to], "Overflow error");

        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;

        emit Transfer(msg.sender, _to, _value);
        return true;
    }
}
'''

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"TestCoin.sol": {"content": contract_source_code}},
    "settings": {"outputSelection": {"": {"": ["metadata", "evm.bytecode", "evm.sourceMap"]}}}
})

bytecode = compiled_sol["contracts"]["TestCoin.sol"]["TestCoin"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["TestCoin.sol"]["TestCoin"]["abi"]

# Deploy contract to Ethereum blockchain
contract = webthree.eth.contract(abi=abi, bytecode=bytecode)

# Deploy contract function
def deploy_contract(initial_supply):
    tx_hash = contract.constructor(initial_supply).transact()
    tx_receipt = webthree.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress
    return contract_address

@app.route('/deploy', methods=['POST'])
def deploy():
    initial_supply = int(request.json['initialSupply'])
    contract_address = deploy_contract(initial_supply)
    return jsonify({"contractAddress": contract_address})

if _name_ == '_main_':
    app.run(debug=True)