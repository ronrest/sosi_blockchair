def wei2eth(wei, decimals=18):
    """Given a WEI value (as string or int), return it as an ETH float value.
    NOTE: there will likely be rounding errors.
    """
    return int(wei) / int(1 * (10 ** decimals))

def wei2ethstr(wei, decimals=18):
    """Given a WEI value (as string or int), return it as an ETH string value.
    This is designed to minimize rounding errors.
    """
    weistr = f"{int(wei):0{decimals}d}"
    ethstr = weistr[:-decimals] + "." + weistr[-decimals:]
    if ethstr[0] == ".":
        ethstr = "0" + ethstr
    return ethstr

def hex2int(x):
    """Given a hex string, return it as an integer value."""
    return int(x, 16)
