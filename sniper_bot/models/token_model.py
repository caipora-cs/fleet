import dataclasses
from sniper_bot.utils.style import style


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

    def __repr__(self) -> str:
        return (
            f"\n\t\tIs Airdrop Scam: {self.is_airdrop_scam}\n"
            f"\t\tIs Anti Whale: {self.is_anti_whale}\n"
            f"\t\tIs Blacklisted: {self.is_blacklisted}\n"
            f"\t\tIs Honeypot: {self.is_honeypot}\n"
            f"\t\tIs In DEX: {self.is_in_dex}\n"
            f"\t\tIs Mintable: {self.is_mintable}\n"
            f"\t\tIs Proxy: {self.is_proxy}\n"
            f"\t\tIs Whitelisted: {self.is_whitelisted}\n"
            f"\t\tSell Tax: {self.sell_tax}\n"
            f"\t\tTrading Cooldown: {self.trading_cooldown}\n"
            f"\t\tTransfer Pausable: {self.transfer_pausable}"
        )


@dataclasses.dataclass
class PriceChange:
    """PriceChange dataclass for TokenData"""

    h1: float
    h24: float
    h6: float
    m5: float

    def __repr__(self) -> str:
        return (
            f"\n\t\tH1: {self.h1}\n"
            f"\t\tH24: {self.h24}\n"
            f"\t\tH6: {self.h6}\n"
            f"\t\tM5: {self.m5}"
        )


@dataclasses.dataclass
class Volume:
    """Volume dataclass for TokenData"""

    h1: float
    h24: float
    h6: float
    m5: float

    def __repr__(self) -> str:
        return (
            f"\n\t\tH1: {self.h1}\n"
            f"\t\tH24: {self.h24}\n"
            f"\t\tH6: {self.h6}\n"
            f"\t\tM5: {self.m5}"
        )


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

    def __repr__(self):
        return (
            style.MAGENTA
            + f"\t\nPair ID: {self.pair_id}\n"
            + style.RESET
            + f"\tTokens: {self.tokens}\n"
            f"\tToken0: {self.token0}\n"
            f"\tToken1: {self.token1}\n"
            f"\tSecurity: {self.security}\n"
            f"\tName: {self.name}\n"
            f"\tSymbol: {self.symbol}\n"
            f"\tFDV: {self.fdv}\n"
            f"\tLiquidity USD: {self.liquidity_usd}\n"
            f"\tCreation Timestamp: {self.creation_timestamp}\n"
            f"\tPrice Change: {self.price_change}\n"
            f"\tVolume: {self.volume}\n"
            f"\tTime Scanned: {self.time_scanned}\n"
            f"\tBuy Signal: {self.buy_signal}\n"
            f"\tWebsite: {self.website}"
        )


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
