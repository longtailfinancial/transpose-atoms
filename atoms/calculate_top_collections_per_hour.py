import os
from multiprocessing.dummy import Pool
from dateutil import parser
from datetime import timedelta
from pprint import pprint

from transpose import Transpose


def calculate_top_collections_per_hour(
    api: Transpose, 
    time: str, 
    num_collections: int = 10):
    """
    Get the top num_collections collections by sale volume for a given hour

    :param api: Transpose API object
    :param time: Time to get top collections for '2022-04-03 12:00:00'
    :param num_collections: Number of collections to return
    :return: List of top collections
    """ 

    # Setup dates
    start_date = parser.parse(time)
    end_date = start_date + timedelta(hours=1)

    # conver dates to str
    start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
    end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")

    # Get all sales for requested hour
    sales = api.bulk_request(api.nft.sales(start_date, end_date, limit=500), 15)
    
    # Aggregate sales volume by collection
    usd_volume_by_collection = {}
    for sale in sales:
        if sale.usd_price is None or sale.is_multi_token_sale:
            continue
        elif sale.contract_address in usd_volume_by_collection: 
            usd_volume_by_collection[sale.contract_address] += sale.usd_price
        else:
            usd_volume_by_collection[sale.contract_address] = sale.usd_price

    # Sort collections by volume
    usd_volume_by_collection = sorted(usd_volume_by_collection.items(), key=lambda x: x[1], reverse=True)
    print("Found {} collections".format(len(usd_volume_by_collection)))

    # Return top collections
    return usd_volume_by_collection[:num_collections]


if __name__ == "__main__":
    key = os.environ["TRANSPOSE_KEY"]
    api = Transpose(key)
    pprint(calculate_top_collections_per_hour(api, "2022-04-03 12:00:00"))