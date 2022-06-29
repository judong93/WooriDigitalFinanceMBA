pragma solidity >0.7.0 <0.8.0;

contract MyToken{
    uint256 public totalSupply; // uint256 == uint
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping(address => uint256)) private approved;

    string public name;
    string public symbol;
    uint256 public decimals;

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);

    constructor (string memory _name, string memory _symbol, 
                 uint256 _supply, uint256 _decimals) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        
        balanceOf[msg.sender] = _supply * 10 ** _decimals;
        totalSupply = _supply * 10 ** _decimals;
    }

    function isValidTransfer(address _from, address _to, uint256 _value) internal view returns (bool isValid) {
        if (balanceOf[_from] >= _value && balanceOf[_to] + _value >= balanceOf[_to]) {
            isValid = true;
        } else {
            isValid = false;
        }

        return isValid;
    }
    
    function transfer(address _to, uint256 _value) public returns (bool success) {
        if (isValidTransfer(msg.sender, _to, _value)) {
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
        if (allowance(_from, msg.sender) > 0 && isValidTransfer(_from, _to, _value)) {
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