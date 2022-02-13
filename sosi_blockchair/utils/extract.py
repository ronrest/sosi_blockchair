import copy

from . import conversions
from . contracts import token_contracts, token_contracts_by_name

def extract_eth_transfer(t, as_eth=False):
    """
    Given the output of calling `client.transaction(tid)`, extract the ethereum
    transfer information.

    Args:
        t:  (dict) transaction information.
        as_eth: (bool) return values as ETH instead of the default WEI.

    Returns:
        sender:       Address
        recipient:    Address
        value:        Value as a string
        fee:          Value as a string
    """
    trx = t["transaction"]
    sender = trx["sender"]
    recipient = trx["recipient"]
    value = trx["value"]
    fee = trx["fee"]

    if as_eth:
        value = conversions.wei2ethstr(value)
        fee = conversions.wei2ethstr(fee)

    return sender, recipient, value, fee


def extract_uniswap_exchange(t, as_eth=False):
    """    
    Given the output of calling `client.transaction(tid, events=True)`, of a 
    transaction that is a uniswap exchange between ETH or ERC20 tokens,
    extract those details.
    
    Args:
        t:  (dict) transaction information.
        as_eth: (bool) return values as ETH instead of the default WEI.

    Returns:
        contract_address (str) eg the uniswap contract address
        in_value        (str) the amount of the input token
        out_value       (str) the amount of the output token
        in_token_name   (str) the ticker code of the input token
        out_token_name  (str) the ticker code of the output token
        fee             (str) the fee paid for the transaction
    """
    default_return_val = None, 0, 0, None, None, 0
    fee = t["transaction"].get("fee", 0)
    events = t.get("events", [])
    if len(events) == 0:
        print("No events data.")
        return default_return_val
    else:
        decoded_events = []
        for item in events:
            _decoded_event = copy.deepcopy(item.get("decoded_event",{}))
            if _decoded_event is None:
                _decoded_event = {}
            _decoded_event["contract"] = item.get("contract")
            decoded_events.append(_decoded_event)

        swap_event = [item for item in decoded_events if item.get("name") == "Swap"]
        transfer_events = [item for item in decoded_events if item.get("name") == "Transfer"]
        if len(swap_event) == 0:
            print("No swap events")
            return default_return_val
        elif len(swap_event) > 1:
            print("Multiple swap events detected.")

        # There can be multiple swaps in order to go from TOKEN_A to TOKEN_B.
        swap_event_in = swap_event[0]
        swap_args_in = swap_event_in.get("arguments")
        swap_args_in = {item.get("name"):item.get("value") for item in swap_args_in}

        # The final swap
        swap_event_out = swap_event[-1]
        swap_args_out = swap_event_out.get("arguments")
        swap_args_out = {item.get("name"):item.get("value") for item in swap_args_out}

        # I think that the `amount0` prefix refers to ETH (but am not actually sure)
        eth_in = swap_args_in.get("amount0In") != "0x0"
        eth_out = swap_args_out.get("amount0Out") != "0x0"
        print("ETH_in" if eth_in else "ETH out" if eth_out else "pure ERC20 transfer, i think")

        # Extract information about intermediate swaps.
        if len(transfer_events) >= 2:
            in_token = transfer_events[0].get("contract")
            out_token = transfer_events[-1].get("contract")
            in_token_details = token_contracts.get(in_token, {})
            out_token_details = token_contracts.get(out_token, {})

            in_token_name = in_token_details.get("name", f"UNKNOWN TOKEN ({in_token})")
            out_token_name = out_token_details.get("name", f"UNKNOWN TOKEN ({out_token})")
            # in_token_decimals = in_token_details.get("decimals", 18)
            # out_token_decimals = out_token_details.get("decimals", 18)

            # Get the intermediate swaps that needed to be done to swap from initial to final token
            intermediate_events = transfer_events[1:-1]
            if len(intermediate_events) > 0:
                intermediate_tokens = [_ievent.get('contract') for _ievent in intermediate_events]
                intermediate_tokens = [token_contracts.get(_itoken, {}).get("name", f"UNKNOWN TOKEN ({_itoken})") for _itoken in intermediate_tokens]
                print(f"Swap involved the following intermediate tokens {intermediate_tokens}")
        else:
            print("Not enough transfer events to extract tokens swapped")
            in_token_name = None
            out_token_name = None

        in_value = swap_args_in["amount0In"] if (swap_args_in["amount1In"] == "0x0") else swap_args_in["amount1In"]
        out_value = swap_args_out["amount0Out"] if (swap_args_out["amount1Out"] == "0x0") else swap_args_out["amount1Out"]
        in_value = conversions.hex2int(in_value)
        out_value = conversions.hex2int(out_value)

        # CONVERT UNITS TO ETH
        if as_eth:
            in_decimals = token_contracts.get(in_token, {}).get("decimals", None)
            out_decimals = token_contracts.get(out_token, {}).get("decimals", None)
            if in_decimals is None:
                print(f"WARNING: No decimals information found for token ({in_token}), assuming 18")
                in_decimals = 18
            if out_decimals is None:
                print(f"WARNING: No decimals information found for token ({out_token}), assuming 18")
                out_decimals = 18
            in_value = conversions.wei2ethstr(in_value, decimals=in_decimals)
            out_value = conversions.wei2ethstr(out_value, decimals=out_decimals)
            fee = conversions.wei2ethstr(fee)
        contract_address = swap_args_out.get("sender")
        return contract_address, in_value, out_value, in_token_name, out_token_name, fee


def extract_erc20_transfer(t, as_eth=False):
    """
    Given the output of calling `client.transaction(tid, events=True)`, of a
    transaction that is a transfer of an ERC20 token from one wallet to another,
    extract those details.

    Args:
        t:  (dict) transaction information.
        as_eth: (bool) return values as ETH instead of the default WEI.

    Returns:
        sender      (str) the address of the sender
        recipient   (str) the address of the recipient
        value       (str) the amount of the token
        token_name  (str) the ticker code of the token
        fee         (str) the fee paid for the transaction (ethereum fee)
    """
    events = t.get("events", [])
    fee = t["transaction"].get("fee", 0)
    default_return_val = None, None, 0, None, 0

    # GET TRANSFER EVENTS
    transfer_events = []
    for item in events:
        decoded_event = item.get("decoded_event")
        if (decoded_event is not None) and (decoded_event.get("name") == "Transfer"):
            transfer_events.append(item)

    if len(transfer_events) == 0:
        print("No transfer events data.")
        return default_return_val
    elif len(transfer_events) > 1:
        print("WARNING: more than one transfer events detected. Using the last one.")

    decoded_event = transfer_events[-1].get("decoded_event", {})
    decoded_event["contract"] = transfer_events[-1].get("contract")
    if decoded_event.get("name") == "Transfer":
        args = decoded_event.get("arguments")
        sender = [arg for arg in args if arg["name"] == "sender"][0]["value"]
        recipient = [arg for arg in args if arg["name"] == "recipient"][0]["value"]
        value = [arg for arg in args if arg["name"] == "value"][0]["value"]
        value = conversions.hex2int(value)

        token_address = decoded_event.get("contract")
        token_details = token_contracts.get(token_address, {})
        token_name = token_details.get("name", f"UNKNOWN TOKEN ({token_address})")

        if as_eth:
            token_decimals = token_details.get("decimals", 18)
            value = conversions.wei2ethstr(value, decimals=token_decimals)
            fee = conversions.wei2ethstr(fee)
        return sender, recipient, value, token_name, fee
    else:
        print("Could not interpret transaction as an ERC 20 transfer")
        return default_return_val


def extract_address_transactions(adddress_response, as_eth=False):
    """Given the output of calling `client.address(wallet)`, it extracts the 
    transactions information. And sorts them by time.
    """
    transactions = adddress_response["transactions"]
    transactions = sorted(transactions, key=lambda x: x["time"])
    if as_eth:
        for t in transactions:
            t["value"] = conversions.wei2ethstr(t.get("value", 0))
    return transactions

