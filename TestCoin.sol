pragma solidity ^0.8.0;

// Import the OpenZeppelin ERC20 contract
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// Inherit from the OpenZeppelin ERC20 contract
contract TestCoin is ERC20 {
    string public name = "TestCoin";
    string public symbol = "TSC";
    uint256 public totalSupply;

    // Override the constructor to set the initial supply
    constructor() ERC20("RetailCoin", "TSC") {
        totalSupply = 1000 * (10 ** uint256(decimals()));
        _mint(msg.sender, totalSupply);
    }

    // Override the transfer function to emit the Transfer event
    function transfer(address _to, uint256 _value) public override returns (bool success) {
        super.transfer(_to, _value);
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    // Optional: Function to check the balance of an address
    function getBalance(address _address) public view override returns (uint256 balance) {
        return balanceOf(_address);
    }
}
