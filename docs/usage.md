# Usage


## Connect to Client

```python
import sosi_blockchair as sb

client = sb.BlockchairEthClient()
# client = sb.BlockchairEthClient(testnet=True)  # connect to Eth testnet
```


## Address Details

Returns summry information about the address, as well as brief information about all the transactions made. 

```python
response = client.address("0x11a1b2c3d4e5f7a8b9c0d2e4f6a7b8c9d0e1f2a3b4a22")
```

[Example response](responses/address.md)

## Transaction Details

Returns details about a transaction, given its hash.

```python
transaction = client.transaction("0x55a1b2c3d4e5f7a8b9c0d2e4f6a7b8c9d0e1f2a3b4a66")

# Also get log events information (note costs extra API credits, but allows 
# extracting valuable information about exchanges and ERC20 token transfers)
transaction = client.transaction("0x55a1b2c3d4e5f7a8b9c0d2e4f6a7b8c9d0e1f2a3b4a66", events=True)
```

[Example transaction response](responses/transaction.md)


```python
# Extract ETH transfer information (for wallet to wallet ETH transactions)
items = sb.utils.extract.extract_eth_transfer(transaction, as_eth=True)
# items = (sender, recipient, value, fee)

# Extract an exchange from one token to another kind of token (on uniswap)
items = sb.utils.extract.extract_uniswap_exchange(transaction, as_eth=True)
# items = (contract, in_val, out_val, in_token, out_token, fee)

# Extract information about a transfer of an ERC20 token from one wallet to another
items = sb.utils.extract.extract_erc20_transfer(transaction, as_eth=True)
# items = (sender, recipient, value, fee)

```