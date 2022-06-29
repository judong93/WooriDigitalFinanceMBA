pragma solidity >= 0.7.0 < 0.8.0;
interface ICalculator {
  
  function getResult(uint, uint) external view returns (uint);
  function getResult() external view returns (bool);
  
}
abstract contract Test1 is ICalculator {
  function getResult(uint a, uint b) external view override returns (uint) {
    uint result = a + b;
    return result;
  }
  function getResult() external view override returns (bool){
    return false;
  }
}
contract Test2 is Test1 {
  constructor() public {}
}

