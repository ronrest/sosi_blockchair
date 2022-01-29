# Usage


## Connect to Client

```python
from sosi_blockchair import BlockchairEthClient

client = BlockchairEthClient()
# client = BlockchairEthClient(testnet=True)  # connect to Eth testnet
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
response = client.transaction("0x55a1b2c3d4e5f7a8b9c0d2e4f6a7b8c9d0e1f2a3b4a66")
```

[Example response](responses/transaction.md)
