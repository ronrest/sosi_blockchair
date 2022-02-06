from . import conversions

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
