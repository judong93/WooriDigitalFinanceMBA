// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.8.0;
contract payableExample {

	// 1. address payable
	address payable owner;
	address subOwner;

	constructor(address _subOwner) {
		owner = msg.sender;
        subOwner = _subOwner;
	}

	// 2. payable modifier
	function deposit() public payable {

	}

	function withdrawOwner(uint _eth) public {
		require(_eth * 1 ether <= address(this).balance);
		owner.transfer(_eth * 1 ether);
		// subOwner.transfer(_eth * 1 ether);		
	}

	// 3. payable(<address>)
	function withdrawSubowner(uint _eth) public {
		payable(subOwner).transfer(_eth * 1 ether);
	}

}