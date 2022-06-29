pragma solidity >0.7.0 <0.8.0;

contract PredictionMarket{
    enum Result{DEFAULT, draw, winA, winB}
	struct Betting{
        Result option;
        uint betted;
    }

    address private owner;
    uint public closingTime;

    mapping(address => Betting) private bettings;
    address[] private participants;
    uint public totalBetted;
    uint[4] public totalBettedOn;

	string public result = "DEFAULT";
    Result private resultInternal;
    uint public rewardMultiplier;       // 10000 means 100.00%

	bool public isResultRealsed;
    bool public isSettled;
	
	modifier onlyOwner() {
		require(owner == msg.sender, 
				"This function can only be called by the contract owner.");
		_;
	}
	modifier onlyBeforeClosing() {
		require(block.timestamp <= closingTime, "The market is closed.");
		_;
	}
    modifier onlyAfterClosing() {
		require(block.timestamp >= closingTime, "The market is not closed yet.");
		_;
	}
	
	constructor(uint _durationInSeconds){
		owner = msg.sender;
        closingTime = block.timestamp + _durationInSeconds;
	}
	
	function bet(uint8 _option) public payable onlyBeforeClosing {
        require(msg.value > 0, "You must bet any amount.");
        require(_option < totalBettedOn.length, "Invalid option.");
        require(_option > 0, "You cannot bet on the default option.");
        
		participants.push(msg.sender);
        bettings[msg.sender].option = Result(_option);
        bettings[msg.sender].betted = msg.value;

        totalBetted += msg.value;
        totalBettedOn[_option] += msg.value;
	}

    function cancel() public onlyBeforeClosing {
        require(bettings[msg.sender].betted > 0, "You did not make a bet.");

        uint refund = bettings[msg.sender].betted;
        if (payable(msg.sender).send(refund)) {
            totalBetted -= refund;
            Result option = bettings[msg.sender].option;
            totalBettedOn[uint8(option)] -= refund;

            bettings[msg.sender].betted = 0;
        }
    }

    function settle() public onlyAfterClosing {
        require(isResultRealsed, "The result is not released yet.");
        
        uint numParticipants = participants.length;

        for (uint i = 0; i < numParticipants; i++){
            address participant = participants[i];
            Betting storage betting = bettings[participant];

            if (betting.option == resultInternal) {
                uint reward = betting.betted * rewardMultiplier / 10000;

                if (payable(participant).send(reward)){
                    totalBettedOn[uint8(resultInternal)] -= betting.betted;
                    bettings[participant].betted = 0;
                }
            } 
        }

        if (totalBettedOn[uint8(resultInternal)] == 0){
            // 'address(this).balance' is the balance of this contract
            payable(owner).transfer(address(this).balance);
            isSettled = true;
        }
    }

	function release() public onlyOwner onlyAfterClosing {
		require(!isResultRealsed, "The result is already released.");

		// WARNING: The value generated from this code is not a random number, 
		//          nor does it meet the requirements to be a pseudo-random number.
		uint num = block.timestamp % 3 + 1;
        resultInternal = Result(num);

		if (num == 1) {
			result = "Draw";
		} else if (num == 2) {
			result = "A wins";
		} else if (num == 3) {
			result = "B wins";
		}
        
        rewardMultiplier = totalBetted * 10000 / totalBettedOn[uint8(resultInternal)];
        isResultRealsed = true;
	}

    // WARNING: For practice, just for in this lecture.
    function imforceClosing() public onlyOwner {
        closingTime = 0;
    }
}