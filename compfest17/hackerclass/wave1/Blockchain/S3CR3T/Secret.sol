// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract Secret {
    bytes32 public constant SECRET = 0x726061b2dddd96177e52d122926939b0608ac99930f2f980c08045e863f6ecf3;
    string public constant ReferedBy = "<REDACTED>";
    uint256 public constant GUESS_FEE = 0.5 ether;
    
    bool public solved;
    
    constructor() {}

    function guess(string calldata sentence, string calldata referrer) external payable {
        require(!solved, "Challenge already solved");
        require(msg.value >= GUESS_FEE, "Insufficient guess fee");
        require(keccak256(abi.encodePacked(sentence)) == SECRET, "OOpsie! you are not allowed to join COMPFEST 17");
        require(keccak256(abi.encodePacked(referrer)) == keccak256(abi.encodePacked(ReferedBy)), "who invited you here?");

        solved = true;
    }

    function hint_1() external pure returns (string memory) {
        return "Format sentence: 'Can i join COMPFEST 17? Here is my secret number: [6-digit number]'";
    }

    function isChallengeSolved() public view returns (bool) {
        return solved;
    }
}