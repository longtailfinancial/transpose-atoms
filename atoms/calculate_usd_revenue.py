import os
from transpose import Transpose
from datetime import datetime




def calculate_usd_revenue(api: Transpose, contract_address: str, from_date: str, to_date: str, fee_rate: float=1.0) -> float:
    """
    Calculate the USD revenue for a contract between two dates.
    """
    from_date = datetime.strptime(from_date, "%Y-%m-%d")
    to_date = datetime.strptime(to_date, "%Y-%m-%d")

    # Get all sales for contract between from_date and to_date
    sales = api.bulk_request(api.nft.sales_by_contract_address(contract_address, from_date, to_date, limit=500), 20, 1000)

    # Calculate USD revenue
    usd_revenue = 0
    for sale in sales:
        usd_revenue += sale.usd_price
    
    return usd_revenue * fee_rate


if __name__ == "__main__":
    key = os.environ["TRANSPOSE_KEY"]
    api = Transpose(key)
    print(calculate_usd_revenue(api, "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D", "2022-02-01", "2022-06-01"))