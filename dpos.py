import json
import eth
import csv
import log
from csv_utils import empty_csv_file
from web3 import Web3

CONTRACT_ADDRESS = '0x00000000000000000000000000000000000000fe'
CSV_HEADER = ['block_number', 'delegator', 'validator', 'amount', 'timestamp']

logger = log.get_logger_instance()

def get_contract_instance():
    if not hasattr(get_contract_instance, 'instance'):
        logger.debug('Getting new DPOS contract instance')
        w3 = eth.get_web3_instance()
        address = Web3.to_checksum_address(CONTRACT_ADDRESS)
        with open('abi/Dpos.json') as json_file:
            abi = json.load(json_file)
        get_contract_instance.instance = w3.eth.contract(address=address, abi=abi)
    return get_contract_instance.instance

def save_event_to_csv_file(csv_file, event):
    block_number = event['blockNumber']
    delegator = Web3.to_checksum_address(event.args['delegator'])
    validator = Web3.to_checksum_address(event.args['validator'])

    w3 = eth.get_web3_instance()
    block = w3.eth.get_block(block_number)
    timestamp = block['timestamp']

    logger.debug(f'Saving event at block {block_number} to csv file')

    with open(csv_file, 'a', newline='') as c:
        writer = csv.DictWriter(c, fieldnames=CSV_HEADER)
        writer.writerow({
            'block_number': block_number,
            'delegator': delegator,
            'validator': validator,
            'amount': event.args['amount'],
            'timestamp': timestamp,
        })

def get_undelegation_events(start_block, end_block):
    dpos_contract = get_contract_instance()
    undelegation_events = dpos_contract.events.Undelegated.create_filter(fromBlock=start_block, toBlock=end_block)
    return undelegation_events.get_all_entries()

def index_events(csv_file):
    empty_csv_file(csv_file, CSV_HEADER)

    ranges = eth.get_block_indexing_range()
    i = 0
    for r in ranges:
        i = i+1

        start_block = r['start_block']
        end_block = r['end_block']

        logger.info(f'{i}/{len(ranges)}: Indexing undelegation events from block {start_block} to block {end_block}')
        for event in get_undelegation_events(start_block, end_block):
            save_event_to_csv_file(csv_file, event)