from transpose import Transpose
from pprint import pprint
import os


def get_recent_token_transfers(api: Transpose, contract_address: str, 
                               limit=10) -> list:

    """
    Find the most recent token transfers for a given token, identified by 
    its contract address.

    :param api: Transpose API object
    :param contract_address: Contract address to get recent token transfers for
    :param limit: Number of recent token transfers to return
    :return: List of recent token transfers
    """
    
    # Handle pagination if limit is more than one request can handle
    if limit > 500:
        recent_transfers = api.bulk_request(api.token.transfers_by_contract_address(contract_address, limit=500, order="desc"), 20, limit)
    
    # Otherwise just make one request
    else:
        recent_transfers = api.token.transfers_by_contract_address(contract_address, limit=limit, order="desc")

    return recent_transfers


if __name__ == "__main__":
    key = os.environ["TRANSPOSE_KEY"]
    api = Transpose(key)

    WETH_CONTRACT_ADDRESS = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
    pprint(get_recent_token_transfers(api, WETH_CONTRACT_ADDRESS, 10))
    