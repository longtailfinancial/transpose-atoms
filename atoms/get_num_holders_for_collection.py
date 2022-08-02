from transpose import Transpose
from datetime import datetime
from pprint import pprint
import os


def get_num_holders_for_collection(api: Transpose, contract_address: str) -> int:
    """
    Get the number of holders for a collection.

    :param api: Transpose API object
    :param contract_address: Contract address to get holders for
    :return: Number of holders
    """

    # Get all holders for collection
    nfts = api.bulk_request(api.nft.owners_by_contract_address(contract_address, limit=500), 20)

    # aggregate holders
    holders = {}
    for nft in nfts:
        if nft.owner in holders:
            holders[nft.owner] += 1
        else:
            holders[nft.owner] = 1

    # Return number of holders
    return len(holders)


if __name__ == "__main__":
    key = os.environ["TRANSPOSE_KEY"]
    api = Transpose(key)

    BAYC_CONTRACT_ADDRESS = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
    pprint(get_num_holders_for_collection(api, BAYC_CONTRACT_ADDRESS))
 