import dataclasses


@dataclasses.dataclass
class Security:
    """Security dataclass for TokenData"""

    is_airdrop_scam: bool
    is_anti_whale: bool
    is_blacklisted: bool
    is_honeypot: bool
    is_in_dex: bool
    is_mintable: bool
    is_proxy: bool
    is_whitelisted: bool
    sell_tax: float
    trading_cooldown: bool
    transfer_pausable: bool


@dataclasses.dataclass
class PriceChange:
    """PriceChange dataclass for TokenData"""

    h1: float
    h24: float
    h6: float
    m5: float


@dataclasses.dataclass
class Volume:
    """Volume dataclass for TokenData"""

    h1: float
    h24: float
    h6: float
    m5: float


@dataclasses.dataclass
class TokenData:
    """TokenData dataclass"""

    pair_id: str
    tokens: list
    token0: str
    token1: str
    security: Security
    name: str
    symbol: str
    fdv: int
    liquidity_usd: float
    creation_timestamp: int
    price_change: PriceChange
    volume: Volume
    time_scanned: str
    buy_signal: bool
    website: str


# Example data
data = {
    "pair_id": "0xaFafFc47072FD2ac75e15D0CA4700852e293725f",
    "tokens": [
        "0x92Ea8f2b711076cC08a734a8e9cD57D3963EbfFf",
        "0x4200000000000000000000000000000000000006",
    ],
    "token0": "0x92Ea8f2b711076cC08a734a8e9cD57D3963EbfFf",
    "token1": "0x4200000000000000000000000000000000000006",
    "security": {"transfer_pausable": "0", "trust_list": None},
    "name": "🐕 Base REX",
    "symbol": "BREX",
    "fdv": 18594,
    "liquidity_usd": 18611.19,
    "creation_timestamp": 1714043589000,
    "price_change": {"h1": 0, "h24": 0, "h6": 0, "m5": 0},
    "volume": {"h1": 0.92, "h24": 0.92, "h6": 0.92, "m5": 0},
    "time_scanned": "2024-04-25 12:13:09",
    "buy_signal": False,
    "website": "https://www.brex.com",
}

token_data = TokenData(**data)
