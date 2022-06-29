// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.8.0;
contract Escrow {
	address public buyer; // address of buyer's wallet
	address public seller; // address of seller's wallet
	address private escrow; // address of intermediary's wallet (private)
	uint private start; // timestamp of contract creation

	bool buyerOk; 
	bool sellerOk; 
    modifier onlyBuyer {
        require(msg.sender == buyer, "Only buyer can call this function");
        _;} 

	constructor(address buyer_address, address seller_address) {
		buyer = buyer_address; 
		seller = seller_address; 
		escrow = msg.sender; 
		start = block.timestamp; 
	}

	function deposit() public payable onlyBuyer{
		
	}

	function payBalance() private {
		payable(escrow).transfer(address(this).balance / 100); // pay a fee for escrow
		payable(seller).transfer(address(this).balance);
	}

	function accept() public {
	
		if (msg.sender == buyer){
			buyerOk = true;
		} else if (msg.sender == seller){
			sellerOk = true;
		}

		if (buyerOk && sellerOk){
			payBalance(); //모두 승인하면 대금 지급
		} else if (buyerOk && !sellerOk && block.timestamp > start + 30 days) {
			selfdestruct(payable(buyer)); // destruct automatically when more than 30 days elapsed with only the buyer's approval
		}
	}

	function cancel() public {
		if (msg.sender == buyer){
			buyerOk = false;
		} else if (msg.sender == seller){
			sellerOk = false;
		} 

		if (!buyerOk && !sellerOk){
			selfdestruct(payable(buyer)); // destruct when the contract is not approved by calling the cancel function
		}
	}

	function kill() public  {
		if (msg.sender == escrow) {
			selfdestruct(payable(buyer)); // destruct if the escrow kill this contract
		}
	}
	function view_balance() public view returns (uint){return address(this).balance;}


}