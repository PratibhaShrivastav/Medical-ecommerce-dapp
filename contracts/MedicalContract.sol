pragma solidity >= 0.4.9;
pragma experimental ABIEncoderV2;

contract MedicalRecords{

    struct Record {
        uint id;
        string name;
        string hospital;
        string doctor;
        string[] medicines;
    }

    mapping(uint => Record) Records;

    uint public totalRecords;

    constructor() public {
        totalRecords = 0;
    }
    
    function addData(string memory _n, string memory _h, string memory _d, string[] memory _medicines) public returns (uint){
        totalRecords++;
        Record memory Singlerecord = Record(totalRecords, _n, _h, _d, _medicines);
        Records[totalRecords] = Singlerecord;
        return totalRecords;
    }

    function recordCount() public view returns (uint) {
        return totalRecords;
    }

    function showData(uint _id) public view returns ( string memory , string memory , string memory, string[] memory) {
        Record memory SingleRecord = Records[_id];
        return (SingleRecord.name, SingleRecord.hospital, SingleRecord.doctor, SingleRecord.medicines);
    }

}