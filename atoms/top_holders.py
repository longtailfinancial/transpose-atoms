from transpose import Transpose


def top_holders(api: Transpose, contract_address: str):
    """
    Get the top holders of a contract.
    """
    # Get all contract holders
    all_holders = api.bulk_request(api.nft.owners_by_contract_address(contract_address, limit=500), 20, 10000)

    # Aggregate holders
    holders = {}
    for holder in all_holders:
        if holder.address not in holders:
            holders[holder.address] = 0
        holders[holder.address] += holder.count

    # Sort holders
    holders = sorted(holders.items(), key=lambda x: x[1], reverse=True)

    # Return top holders
    return holders[:10]