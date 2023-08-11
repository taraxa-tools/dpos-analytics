from web3 import Web3
import log

logger = log.get_logger_instance()

def get_web3_instance():
    if not hasattr(get_web3_instance, 'instance'):
        logger.debug('Getting new web3 instance')
        get_web3_instance.instance = Web3(Web3.WebsocketProvider(f'wss://ws.mainnet.taraxa.io'))
    return get_web3_instance.instance

def get_latest_block_number():
    w3 = get_web3_instance()
    latest_block = w3.eth.get_block('latest')
    return latest_block['number']

def get_block_indexing_range():
    start = 0
    end = get_latest_block_number()
    chunk_size = 1000

    r = []

    for start_block in range(start, end, chunk_size):
        end_block = min(start_block+chunk_size-1, end)
        r.append({'start_block': start_block, 'end_block': end_block})

    return r