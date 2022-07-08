from transpose import Transpose
from pprint import pprint
import os

# Transpose Atom Dependencies
from atoms.get_top_collection_holders import get_top_collection_holders


def get_similar_collections_by_holders(api: Transpose, contract_address: str, 
                                       num_to_return: int=5) -> list:
                            
    """
    Produces a list of similar collections for a given collection, identified by contract 
    address, determined by looking at other NFTs that the top collection holders are holding.

    Collections are deemed similar when top holders in one collection are top holders in another.

    :atom-dependencies: top_holders

    :param api: Transpose API object
    :param contract_address: Contract address to get similar collections for
    :param num_to_return: Number of collections to return
    :return: List of similar collection addresses
    """
    
    # Get top holders for contract
    top_holders_for_contract = get_top_collection_holders(api, contract_address, 5)

    # Retrieve all NFTs owned by each top holder
    top_owned_collections = {}
    for top_holder in top_holders_for_contract:
        owned_nfts = api.bulk_request(api.nft.nfts_by_owner(top_holder[0], limit=500))
    
        # Get the contract address for each NFT and save the number of NFTs owned by each holder
        for nft in owned_nfts:
            if nft.contract_address in top_owned_collections: top_owned_collections[nft.contract_address] += 1
            else: top_owned_collections[nft.contract_address] = 1

    # Sort top owned collections by number of NFTs owned
    sorted_contract_addresses = sorted(top_owned_collections.items(), key=lambda x: x[1], reverse=True)[:num_to_return]

    # Lookup collections for contract addresses
    contract_names = []
    for contract_address in sorted_contract_addresses:
        collections = api.nft.collections_by_contract_address(contract_address[0])
        if len(collections) > 0 and collections[0].name is not None:
            name = collections[0].name
            contract_names.append(name)

    return contract_names


if __name__ == "__main__":
    key = os.environ["TRANSPOSE_KEY"]
    api = Transpose(key)

    BAYC_CONTRACT_ADDRESS = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
    pprint(get_similar_collections_by_holders(api, BAYC_CONTRACT_ADDRESS))