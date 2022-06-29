pragma solidity >0.7.0 <0.8.0;

contract MyTokenWithFeatures{
    uint256 public totalSupply; // uint256 == uint
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping(address => uint256)) private approved;

    string public name;
    string public symbol;
    uint256 public decimals;

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);

    // For the blacklist and membership
    address public manager;
    modifier onlyManager() {
        require(msg.sender == manager, "Only the manager can call this function.");
        _;
    }

    // Blacklist
    mapping (address => uint8) public blacklist;

    event Blacklisted(address indexed _address);
    event DeletedFromBlacklist(address indexed _address);
    event RejectedPaymentToBlacklistedAddr(address indexed _from, address indexed _to, uint256 _value);
    event RejectedPaymentFromBlacklistedAddr(address indexed _from, address indexed _to, uint256 _value);

    // Membership
    mapping (address => uint8) public memberships;
    uint256 public cashbackRate;    // 0-100, 100 means 100%

    event Cashback(address indexed _from, address indexed _to, uint256 _cashback);

    constructor (string memory _name, string memory _symbol, 
                 uint256 _supply, uint256 _decimals) {
        manager = msg.sender;
        
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        
        balanceOf[msg.sender] = _supply * 10 ** _decimals;
        totalSupply = _supply * 10 ** _decimals;
    }

    function isBlacklisted(address _address) public view returns (bool inBlacklist) {
        inBlacklist = blacklist[_address] == 1;
		return inBlacklist;
    }
    function pushBlacklist(address _address) public onlyManager {
        blacklist[_address] = 1;
        emit Blacklisted(_address);
    }
    function deleteFromBlacklist(address _address) public onlyManager {
        blacklist[_address] = 0;
        emit DeletedFromBlacklist(_address);
    }

    function setMembership(address _address, uint8 _isMember) public onlyManager {
        memberships[_address] = _isMember;
    }
    function setCashbackRate(uint256 _cashbackRate) public onlyManager {
        require(_cashbackRate >= 0 && _cashbackRate <= 100, "Invalid cashback rate.");
        cashbackRate = _cashbackRate;
    }

    function isValidTransfer(address _from, address _to, uint256 _value) 
    internal view returns (bool isValid) {
        if (balanceOf[_from] >= _value && balanceOf[_to] + _value >= balanceOf[_to]) {
            isValid = true;
        } else {
            isValid = false;
        }

        return isValid;
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        if (isBlacklisted(msg.sender)) {
            emit RejectedPaymentFromBlacklistedAddr(msg.sender, _to, _value);
            success = false;
        } else if (isBlacklisted(_to)) {
            emit RejectedPaymentToBlacklistedAddr(msg.sender, _to, _value);
            success = false;
        } else if (isValidTransfer(msg.sender, _to, _value)) {
            if (_to == manager) {
                uint256 cashback = _value * cashbackRate / 100;
                _value -= cashback;
                emit Cashback(msg.sender, _to, cashback);
            }

            balanceOf[msg.sender] -= _value;
            balanceOf[_to] += _value;
            
            emit Transfer(msg.sender, _to, _value);
            success = true;
        } else {
            success = false;
        }

        return success;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        if (approved[msg.sender][_spender] + _value >= approved[msg.sender][_spender]) {
            approved[msg.sender][_spender] = approved[msg.sender][_spender] + _value;

            emit Approval(msg.sender, _spender, _value);
            success = true;
        } else {
            success = false;
        }
    }

    function allowance(address _owner, address _spender) public view returns (uint256 remaining) {
        remaining = approved[_owner][_spender];
        return remaining;
    }
	
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (isBlacklisted(_from)) {
            emit RejectedPaymentFromBlacklistedAddr(_from, _to, _value);
            success = false;
        } else if (isBlacklisted(_to)) {
            emit RejectedPaymentToBlacklistedAddr(_from, _to, _value);
            success = false;
        } else if (allowance(_from, msg.sender) > 0 && isValidTransfer(_from, _to, _value)) {
            if (_to == manager) {
                uint256 cashback = _value * cashbackRate / 100;
                _value -= cashback;
                emit Cashback(msg.sender, _to, cashback);
            }

            balanceOf[_from] -= _value;
            balanceOf[_to] += _value;
            approved[_from][msg.sender] -= _value;

            emit Transfer(_from, _to, _value);
            success = true;
        } else {
            success = false;
        }

        return success;
    }
}