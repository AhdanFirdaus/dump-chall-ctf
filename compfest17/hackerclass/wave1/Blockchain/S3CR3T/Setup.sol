// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Secret.sol";

contract Setup {
    Secret public challenge;

    constructor() payable {
        challenge = new Secret();
    }

    function isSolved() external view returns (bool) {
        return challenge.isChallengeSolved();
    }
}