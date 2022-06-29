from transpose import Transpose


def recent_token_transfers(api: Transpose, contract_address, limit=10):
    # Handle pagination if limit is more than one request can handle
    if limit > 500:
        recent_transfers = api.bulk_request(api.transfers_by_contract_address(contract_address, 500, order="desc"), 20, limit)
    
    # Otherwise just make one request
    else:
        recent_transfers = api.token.transfers_by_contract_address(contract_address, limit, order="desc")

    print("Found {} transfers".format(len(recent_transfers)))
    return recent_transfers