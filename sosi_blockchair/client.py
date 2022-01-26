"""
blockchair.com API
    https://blockchair.com/api/docs


RATE LIMITS
-------
https://blockchair.com/api/docs#link_M05
- Soft limit of 5 requests per second on both free and paid plans.
  A 435 ERROR will be returned if you hit this limit.
- Hard Limit of 30 requests/min. on the free plan.
  A 402 or 429 ERROR will be returned if you hit this limit.
- If you have exceeded the limit multiple times without using a key, a 
  430, 434, or 503 ERROR may be returned meaning that you've been blocked.
- Max of 1,000 calls per day on free plan.
  Once you go over the limit, your IP-address will be blocked from using the 
  free API.
  QUESTION: will it be blocked forever? Or for the rest of that day?
- Higher limits apply to paid plans.
  https://blockchair.com/api/plans

- The daily request counter is reset at 00:00 UTC every day.
- Majority of queries are counted as 1. Some queries, such as batch queries 
  for blocks, transactions, addresses, and mass address balance checks have a 
  higher request count.

- Every API response yields context.request_cost with the request cost number 
  ("request points").

"""
from copy import deepcopy
from sosi_api import BaseClient
from sosi_api.utils import dt as dtutils
import decouple
# import datetime

from . utils.status_handlers import DEFAULT_STATUS_HANDLERS

env = decouple.AutoConfig(search_path="./.env")
# from urllib.parse import urlencode

class BlockchairEthClient(BaseClient):
    def __init__(self, key=None, testnet=False):
        chain_subdir = "ethereum/testnet" if testnet else "ethereum"
        super().__init__(
            base_url=f"https://api.blockchair.com/{chain_subdir}",
            headers=None,
            max_requests_per_min=30,
            response_kind="json",
            status_handlers=DEFAULT_STATUS_HANDLERS,
        )
        self.api_key = key if key is not None else env('BLOCKCHAIR_API_KEY', default=None)

    def request(self, url=None, endpoint=None, params=None, headers=None, kind="get", response_kind=None):
        if self.api_key is not None:
            params = deepcopy(params) if params is not None else dict()
            params["api_key"] = self.api_key
        response = self._request(url=url, endpoint=endpoint, params=params, headers=headers, kind=kind, response_kind=response_kind)
        return response

    def address(self, address, erc20=True, usd_balance=False, contract_details=False, verbose=True):
        """Get summary information for a wallet address.
        
        Args:
            address (str): Wallet address
            erc20 (bool, list of str): Include ERC20 tokens? Optionally provide 
                list of tokens to include.
                QUESTION: does it cost more API calls to include all ERC20 tokens?
            usd_balance (bool): Include USD balance?
            contract_details (bool): Include contract details like token name, 
                symbol, decimals, etc. Costs an extra 0.5 API call.

        Returns:
            Dict with the following keys:
            - summary: (dict) summary info about wallet.
            - transactions: (list of dict) overview of all transactions.
        """
        endpoint = f"/dashboards/address/{address}"
        params = dict()
        if erc20 == True:
            params["erc20"] = "true"
        elif isinstance(erc20, (list, tuple)):
            params["erc20"] = ",".join(erc20)
        else:
            params["erc20"] = erc20

        if usd_balance:
            params["assets_in_usd"] = "true"
        if contract_details:
            params["contract_details"] = "true"

        response = self.request(endpoint=endpoint, params=params, kind="get")

        # EXTRACT API CALL METADATA
        context = response.get("context", {})
        limit = context.get("limit")    # eg '100,100'
        offset = context.get("offset")   # eg '0,0'
        n_results = context.get("results")  # number of results
        cost = context.get("request_cost") # eg 1
        if verbose:
            print(f"cost: {cost} n results: {n_results} (limit {limit}  offset {offset})")

        # EXTRACT DATA
        data = response.get("data",{}).get(address.lower(), {})
        transactions = data.get("calls", []) # List of transactions (including internal ones)
        summary = data.get("address", {})

        output = dict()
        output["summary"] = summary
        output["transactions"] = transactions
        return output

    def transaction(self, hash, erc20=True, effects=True, verbose=True):
        """Get information for a transaction given its transaction hash id
        
        Returns: 
            Dict with the following keys:
            - calls:       list of dicts of internal transactions?
            - effects:     dict 
            - transaction: dict 

        """
        endpoint = f"/dashboards/transaction/{hash}"
        params = dict()

        params["trace_mempool"] = "true"
        if erc20 == True:
            params["erc20"] = "true"
        if effects == True:
            params["effects"] = "true"

        response = self.request(endpoint=endpoint, params=params, kind="get")

        # EXTRACT API RESPONSE METADATA
        context = response.get("context", {})
        n_results = context.get("results")
        cost = context.get("request_cost")
        if verbose:
            print(f"cost: {cost} n results: {n_results}")

        # EXTRACT DATA
        data = response.get("data", {}).get(hash.lower(), {})
        return data
