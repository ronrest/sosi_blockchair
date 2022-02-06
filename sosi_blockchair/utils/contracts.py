token_contracts = {
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2":{"name": "WETH", "decimals":18},
    "0xcdeee767bed58c5325f68500115d4b722b3724ee":{"name": "CRBN", "decimals":18},
    "0xdac17f958d2ee523a2206206994597c13d831ec7":{"name": "USDT", "decimals":18},
    "0x7968bc6a03017ea2de509aaa816f163db0f35148":{"name": "HGET", "decimals":6},
    "0x3f382dbd960e3a9bbceae22651e88158d2791550":{"name": "GHST", "decimals":18},
    "0x10be9a8dae441d276a5027936c3aaded2d82bc15":{"name": "UMX", "decimals":18},
    "":{"name": "ETH", "decimals":18},
}
token_contracts_by_name = {val.get("name"): {"address": key, **val} for key, val in token_contracts.items()}
