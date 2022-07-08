from transpose import Transpose

# Transpose Atom Dependencies
from atoms.calculate_top_holders import calculate_top_holders


def get_similar_collections(api: Transpose, contract_address: str, num_to_return: int = 5):
    """
    Returns a list of similar collections for a given contract address.

    Collections are deemed similar when top holders in one collection are top holders in another.

    :atom-dependencies: top_holders

    :param api: Transpose API object
    :param contract_address: Contract address to get similar collections for
    :param num_to_return: Number of collections to return
    :return: List of similar collection addresses
    """
    
    # Get top holders for contract
    top_holders_for_contract = calculate_top_holders(api, contract_address, 5)
    print("Found {} top holders".format(len(top_holders_for_contract)))

    # Retrieve all NFTs owned by each top holder
    top_owned_collections = {}
    for top_holder in top_holders_for_contract:
        print("Getting NFTs owned by {}".format(top_holder[0]))
        owned_nfts = api.bulk_request(api.nft.nfts_by_owner(top_holder[0], limit=500))
    
        # get the contract address for each NFT and save the number of NFTs owned by each holder
        for nft in owned_nfts:
            if nft.contract_address in top_owned_collections: top_owned_collections[nft.contract_address] += 1
            else: top_owned_collections[nft.contract_address] = 1

    print("Found {} Collections owned by top holders".format(len(top_owned_collections)))

    # Sort top owned collections by number of NFTs owned
    sorted_contract_addresses = sorted(top_owned_collections.items(), key=lambda x: x[1], reverse=True)[:num_to_return]

    named_contracts = {}
    for contract_address in sorted_contract_addresses:
        name = api.nft.collections_by_contract_address(contract_address[0])[0].name
        named_contracts[name] = contract_address[1]

    return named_contracts


if __name__ == "__main__":
    import os
    import json

    key = os.environ["TRANSPOSE_KEY"]
    api = Transpose(key)
    BAYC_CONTRACT_ADDRESS = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
    print(json.dumps(get_similar_collections(api, BAYC_CONTRACT_ADDRESS), indent=4))