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
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    // Optional: Function to check the balance of an address
    function getBalance(address _address) public view returns (uint256 balance) {
        return balanceOf[_address];
    }
}