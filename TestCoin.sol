// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

// Import OpenZeppelin Contracts using the correct path
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title TestCoin
 * @dev Simple ERC20 Token example, where all tokens are pre-assigned to the creator.
 */
contract TestCoin is ERC20, Ownable {

    /**
     * @dev Constructor that gives msg.sender all of existing tokens.
     */
    constructor () ERC20("TestCoin", "TSC") {
        _mint(msg.sender, 1000 * 10 ** uint256(decimals()));
    }
}
