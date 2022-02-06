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

contract_names = {
    "0x7a250d5630b4cf539739df2c5dacb4c659f2488d": "Uniswap V2: Router 2",
    "0x61122b41600c59ef4248ff9818fbf0a1b43abe17": "Uniswap V2: CRBN 3", # uniswap contract for exchanging carbon CRBN tokens
    "0x4d5ebb22982ffeccb7b3e42a624555cb313285f0": "Uniswap V2: HGET-USDT 2", # uniswap contract for swapping HGET and USDT
    "0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852": "Uniswap V2: USDT", # Uniswap contract for swapping ETH with USDT
    "0xa0c68c638235ee32657e8f720a23cec1bfc77c77": "Polygon (Matic): Bridge", # For bridging between ethereum and polygon networks
    "0x40ec5b33f54e0e8a33a975908c5ba1c14e5bbbdf": "Polygon (Matic): ERC20 Bridge", # For bridging ERC20 tokens between ethereum and polygon networks
}
