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
    transaction that is a uniswap exchange between ETH and an ERC20 token,
    extract those details.
    
    Args:
        t:  (dict) transaction information.
        as_eth: (bool) return values as ETH instead of the default WEI.

    Returns:
        contract_address
        in_value
        out_value
        in_token_name
        out_token_name
        fee
    """
    fee = t["transaction"].get("fee", 0)
    events = t.get("events", [])
    if len(events) == 0:
        print("No events data.")
        return None, 0, 0, None, None
    else:
        decoded_events = []
        for item in events:
            _decoded_event = copy.deepcopy(item.get("decoded_event",{}))
            _decoded_event["contract"] = item.get("contract")
            decoded_events.append(_decoded_event)

        swap_event = [item for item in decoded_events if item.get("name") == "Swap"]
        transfer_events = [item for item in decoded_events if item.get("name") == "Transfer"]
        if len(swap_event) == 0:
            print("No swap events")
            return None, 0, 0, None, None
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
