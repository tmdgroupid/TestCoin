// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract TestCoin is ERC20 {
    constructor() ERC20("TestCoin", "TSC") {
        _mint(msg.sender, 1000 * (10 ** uint256(decimals())));
    }
}
