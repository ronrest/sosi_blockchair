# Example Address Response


```python
{
    'summary': {
        'type': 'account',
        'contract_code_hex': None,
        'contract_created': None,
        'contract_destroyed': None,
        'balance': '1234567890123',
        'balance_usd': 44.12345678901234,
        'received_approximate': '1234567890123456',
        'received_usd': 12464.1017,
        'spent_approximate': '12345678901234567890',
        'spent_usd': 12345.12345,
        'fees_approximate': '123456789012',
        'fees_usd': 123.456,
        'receiving_call_count': 1,
        'spending_call_count': 3,
        'call_count': 4,
        'transaction_count': 4,
        'first_seen_receiving': '2022-01-01 10:15:55',
        'last_seen_receiving': '2022-10-21 08:35:56',
        'first_seen_spending': '2022-01-01 10:15:56',
        'last_seen_spending': '2022-10-01 10:15:55',
        'nonce': None
    },
    'transactions': [
        {
            'block_id': 12345678,
            'transaction_hash': '0xa1b2c3d4e5f7a8b9c0d2e4f6a7b8c9d0e1f2a3b4c5',
            'index': '0',
            'time': '2022-01-01 10:16:55',
            'sender': '0x11a1b2c3d4e5f7a8b9c0d2e4f6a7b8c9d0e1f2a3b4a22',
            'recipient': '0x33a1b2c3d4e5f7a8b9c0d2e4f6a7b8c9d0e1f2a3b4a44',
            'value': 0,
            'value_usd': 0,
            'transferred': True
        }, {
            'block_id': 12345679,
            'transaction_hash': '0xa1b2c3d4e5f7a8b9c0d2e4f6a7b8c9d0e1f2a3b4c5',
            'index': '0.0.1',
            'time': '2022-01-01 10:18:55',
            'sender': '0x55a1b2c3d4e5f7a8b9c0d2e4f6a7b8c9d0e1f2a3b4a66',
            'recipient': '0x77a1b2c3d4e5f7a8b9c0d2e4f6a7b8c9d0e1f2a3b4a88',
            'value': 0,
            'value_usd': 0,
            'transferred': True
        },

        ...
        
    ]
}
```