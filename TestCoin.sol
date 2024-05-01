// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract RetailCoin is ERC20 {
    constructor() ERC20("RetailCoin", "RTC") {
        _mint(msg.sender, 1000 * (10 ** uint256(decimals())));
    }
}
