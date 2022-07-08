from transpose import Transpose
from pprint import pprint
import os


def get_collection_mint_prices(api: Transpose, contract_address: str,
                               limit: int=10) -> list:

    """
    Get the mint prices for a collection, identified by its contract address. Doesn't
    handle massive scale well just yet but will add this soon! (updated: 7/8/22)

    Returns:
        [{
            'transaction_hash': transaction_hash,
            'nft': (contract_address, token_id),
            'minter': minter_address,
            'mint_price': mint_value_eth
        }]

    :param api: Transpose API object
    :param contract_address: Contract address to get collection mint prices for
    :param limit: Number of mints to return
    :return: List of top holders
    """

    # Get all mints
    mints = api.nft.transfers_by_contract_address(
        contract_address=contract_address, 
        transfer_category='mint',
        limit=min(limit + 10, limit)
    )

    # Group mints by transaction hash
    mints_by_transaction = {}
    last_transaction_hash = mints[-1].transaction_hash
    for mint in mints:
        if mint.transaction_hash == last_transaction_hash: 
            continue
        elif mint.transaction_hash in mints_by_transaction:
            mints_by_transaction[mint.transaction_hash].append(mint)
        else:
            mints_by_transaction[mint.transaction_hash] = [mint]

    # Lookup transactions
    transactions = api.block.transactions_by_hash(transaction_hashes=list(mints_by_transaction.keys()))
    value_by_transaction = {transaction.transaction_hash: transaction.value for transaction in transactions}

    # Group mints data
    mints_data = []
    for transaction_hash, mints in mints_by_transaction.items():
        mint_value_wei = value_by_transaction[transaction_hash] / len(mints)
        mint_value_eth = mint_value_wei / 10 ** 18

        for mint in mints:
            mints_data.append({
                'transaction_hash': transaction_hash,
                'nft': (mint.contract_address, mint.token_id),
                'minter': mint.to,
                'mint_price': mint_value_eth
            })

    # Return enriched mint data
    return mints_data


if __name__ == "__main__":    
    key = os.environ["TRANSPOSE_KEY"]
    api = Transpose(key)

    bayc_contract_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
    pprint(get_collection_mint_prices(api, bayc_contract_address, limit=100))