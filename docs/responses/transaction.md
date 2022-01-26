# Example Transaction Response

```python
{
    'transaction': {
        'block_id': 14080221,
        'id': 14080221000008,
        'index': 8,
        'hash': '0xefd85cc54057c2fc6a92f8ab06aa79d4b1e5d4a063154eff21d67f9541354034',
        'date': '2022-01-26',
        'time': '2022-01-26 08:42:35',
        'failed': False,
        'type': 'call',
        'sender': '0xd24400ae8bfebb18ca49be86258a3c749cf46853',
        'recipient': '0xe3c6799929034ca3089e992fa6ce97f3a9b24c57',
        'call_count': 1,
        'value': '356907000000000000',
        'value_usd': 876.950299340332,
        'internal_value': '356907000000000000',
        'internal_value_usd': 876.950299340332,
        'fee': '2149098005628000',
        'fee_usd': 5.28051324111655,
        'gas_used': 21000,
        'gas_limit': 90000,
        'gas_price': 102338000268,
        'input_hex': '',
        'nonce': 2652533,
        'v': '26',
        'r': '9d5914ec8f0b2831eecb315c883486fa6654feb74da50921df09a4f9b322321c',
        's': '609153cfd76d9881a6f3102c4b071f0e435411d93d47c8f979b080d5fa67d88f',
        'version': 0,
        'effective_gas_price': 102338000268,
        'max_fee_per_gas': None,
        'max_priority_fee_per_gas': None,
        'base_fee_per_gas': 83484679753,
        'burned': '1753178274813000',
        'type_2718': 0,
        'miner': '0xd757fd54b273bb1234d4d9993f27699d28d0edd2'
    },
    'calls': [
        {
            'block_id': 14080221,
            'transaction_id': 14080221000008,
            'transaction_hash': '0xefd85cc54057c2fc6a92f8ab06aa79d4b1e5d4a063154eff21d67f9541354034',
            'index': '0',
            'depth': 0,
            'date': '2022-01-26',
            'time': '2022-01-26 08:42:35',
            'failed': False,
            'fail_reason': None,
            'type': 'call',
            'sender': '0xd24400ae8bfebb18ca49be86258a3c749cf46853',
            'recipient': '0xe3c6799929034ca3089e992fa6ce97f3a9b24c57',
            'child_call_count': 0,
            'value': '356907000000000000',
            'value_usd': 876.950299340332,
            'transferred': True,
            'input_hex': '',
            'output_hex': ''
        }],
    'effects': {
        '0x0000000000000000000000000000000000000000': {
            'asset_type': 'native',
            'asset_name': 'Ethereum',
            'asset_symbol': 'ETH',
            'asset_decimals': 18,
            'changes': {
                '0xd24400ae8bfebb18ca49be86258a3c749cf46853': '-359056098005628000',
                '0xd757fd54b273bb1234d4d9993f27699d28d0edd2': '2149098005628000',
                '0xe3c6799929034ca3089e992fa6ce97f3a9b24c57': '356907000000000000'
            }
        }
    }
}
```