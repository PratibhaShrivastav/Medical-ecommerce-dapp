from web3 import Web3
from solc import compile_standard
import glob
import json

"""
Loading contents of Medical.json which needs to be deployed to Blockchain
"""
f = glob.glob('Medical.json')
content = json.load(open(f[0], "r"))

"""
1. Creating Web3 instance
"""
web3Instance = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

"""
This function will be executed only once for deploying our 
contracts on Blockchain.
"""
def deploy_contract(contract_interface):
    
    # Instantiate and deploy contract
    contract = web3Instance.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['evm']['bytecode']['object']
        )
    
    tx_hash = contract.deploy(transaction={'from': web3Instance.eth.accounts[1]})   # Get transaction hash from deployed contract
    tx_receipt = web3Instance.eth.getTransactionReceipt(tx_hash)                    # Get tx receipt to get contract address
    return tx_receipt['contractAddress']


"""
2. Compiling the contract(.sol) files
----------------------------------
Multiple files can be passed as array ['a.sol','b.sol']
"""
contracts = compile_standard(content, allow_paths='/', bin=True)                    #Compiling using solc compiler
MedicalContract = contracts["contracts"]["MedicalRecords.sol"]["MedicalRecords"]    #Selecting relevant data from output of Compile function

contract_address = deploy_contract(MedicalContract)                                 #Deploying the Contract on Blockchain


"""
Saving Contents to data.json
We need to remember the contract address and abi of the deployed contract
to be able to interact with it afterwords.
"""
with open('data.json', 'w') as outfile:
    data = {
        "abi" : MedicalContract['abi'],
        "contract_address" : contract_address
    }
    json.dump(data, outfile, indent=4, sort_keys=True)

print("Contract deployed successfully at ", contract_address)