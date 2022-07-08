from transpose import Transpose


def calculate_top_holders(api: Transpose, contract_address: str, num_holders: int = 10):
    """
    Get the top holders of a contract.

    :param api: Transpose API object
    :param contract_address: Contract address to get top holders for
    :param num_holders: Number of top holders to return
    :return: List of top holders=
    """

    # Get all contract holders
    all_holders = api.bulk_request(api.nft.owners_by_contract_address(contract_address, limit=500), 15)

    # Aggregate holders
    holders = {}
    for holder in all_holders:
        if holder.owner not in holders:
            holders[holder.owner] = 0
        holders[holder.owner] += holder.balance

    # Sort holders
    holders = sorted(holders.items(), key=lambda x: x[1], reverse=True)
    print("Found {} holders".format(len(holders)))

    # Return top holders
    return holders[:num_holders]


if __name__ == "__main__":
    import os
    from pprint import pprint
    
    key = os.environ["TRANSPOSE_KEY"]
    api = Transpose(key)
    bayc_contract_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
    pprint(calculate_top_holders(api, bayc_contract_address))