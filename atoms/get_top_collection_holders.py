from transpose import Transpose
from pprint import pprint
import os


def get_top_collection_holders(api: Transpose, contract_address: str,
                               num_holders: int=10) -> list:

    """
    Get the top holders of a NFT collection by number of NFTs owned, including
    quantity in the case of ERC-1155 NFTs.

    :param api: Transpose API object
    :param contract_address: Contract address to get top holders for
    :param num_holders: Number of top holders to return
    :return: List of top holders
    """

    # Get all contract holders
    all_holders = api.bulk_request(api.nft.owners_by_contract_address(contract_address, limit=500), 20, 500)

    # Aggregate holders
    holders = {}
    for holder in all_holders:
        if holder.owner not in holders:
            holders[holder.owner] = 0
        holders[holder.owner] += holder.balance

    # Sort holders
    holders = sorted(holders.items(), key=lambda x: x[1], reverse=True)

    # Return top holders
    return holders[:num_holders]


if __name__ == "__main__":    
    key = os.environ["TRANSPOSE_KEY"]
    api = Transpose(key)

    bayc_contract_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
    pprint(get_top_collection_holders(api, bayc_contract_address))