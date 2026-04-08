"""known router and aggregator addresses."""

from __future__ import annotations

from typing import Dict


KNOWN_ROUTERS: Dict[str, str] = {
    "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D": "uniswap-v2-router",
    "0xE592427A0AEce92De3Edee1F18E0157C05861564": "uniswap-v3-router",
    "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45": "uniswap-v3-router-2",
}


def is_known_router(address: str) -> bool:
    if not address:
        return False
    return address in KNOWN_ROUTERS or address.lower() in {
        k.lower() for k in KNOWN_ROUTERS
    }


def router_label(address: str) -> str:
    if not address:
        return ""
    if address in KNOWN_ROUTERS:
        return KNOWN_ROUTERS[address]
    for k, v in KNOWN_ROUTERS.items():
        if k.lower() == address.lower():
            return v
    return ""
