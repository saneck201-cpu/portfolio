"""Pure helper functions for the bot (no Telegram dependency, easy to test)."""
import re

_UNITS = {"s": 1, "m": 60, "h": 3600, "d": 86400}
_DELAY_RE = re.compile(r"^(\d+)([smhd])$", re.IGNORECASE)
MAX_DELAY = 7 * 86400  # one week


def parse_delay(value: str) -> int:
    """Convert '30s', '10m', '2h', '1d' to seconds.

    Raises ValueError for bad input or delays that are zero / longer than a week.
    """
    match = _DELAY_RE.match(value.strip())
    if not match:
        raise ValueError("Use a number and a unit: 30s, 10m, 2h or 1d")
    seconds = int(match.group(1)) * _UNITS[match.group(2).lower()]
    if seconds <= 0:
        raise ValueError("Delay must be greater than zero")
    if seconds > MAX_DELAY:
        raise ValueError("Maximum delay is 7 days")
    return seconds


def humanize(seconds: int) -> str:
    """90 -> '1m 30s', 3600 -> '1h'."""
    parts = []
    for name, size in (("d", 86400), ("h", 3600), ("m", 60), ("s", 1)):
        qty, seconds = divmod(seconds, size)
        if qty:
            parts.append(f"{qty}{name}")
    return " ".join(parts) or "0s"


def extract_rate(data: dict, code: str) -> float:
    """Get the price of ONE unit of a currency in rubles from the CBR daily JSON."""
    code = code.upper()
    valutes = data.get("Valute", {})
    if code not in valutes:
        raise KeyError(f"Unknown currency: {code}")
    item = valutes[code]
    return item["Value"] / item["Nominal"]
