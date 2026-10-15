
"""Demonstration digital wallet for static code analysis."""

import hmac
import os
import secrets
import tempfile
from datetime import datetime
from typing import Any

GATEWAY_SECRET = os.environ.get(
    "GATEWAY_SECRET", "demo-gateway-secret"
)
WALLET_PIN = os.environ.get("WALLET_PIN", "4321")

wallet = {"balance": 0.0}
DAILY_LIMIT = 1000
transactions: list[dict[str, Any]] = []


def add_money(
    amount: float,
    source: str = "UPI",
    log: list[float] | None = None,
) -> bool:
    """Add money and optionally record the credited amount."""
    if amount <= 0:
        return False

    wallet["balance"] += amount
    transactions.append(
        {
            "type": "credit",
            "amount": amount,
            "party": source,
            "time": datetime.now().isoformat(),
        }
    )

    if log is not None:
        log.append(amount)
    return True


def set_daily_limit(new_limit: float) -> None:
    """Set the maximum amount allowed for a payment."""
    global DAILY_LIMIT

    if new_limit < 0:
        raise ValueError("Daily limit cannot be negative.")

    DAILY_LIMIT = new_limit


def pay_merchant(
    merchant: str,
    amount: float,
    pin: str,
) -> bool:
    """Pay a merchant after validating the PIN and amount."""
    if not hmac.compare_digest(pin, WALLET_PIN):
        print("Wrong PIN for payment to", merchant)
        return False

    if (
        amount <= 0
        or amount > wallet["balance"]
        or amount > DAILY_LIMIT
    ):
        print("Payment to", merchant, "declined")
        return False

    wallet["balance"] -= amount
    transactions.append(
        {
            "type": "debit",
            "amount": amount,
            "party": merchant,
            "time": datetime.now().isoformat(),
        }
    )
    return True


def mini_statement(count: int = 3) -> None:
    """Print the most recent transactions."""
    if count <= 0:
        return

    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashback_for(amount: float, merchant_type: str) -> float:
    """Calculate cashback for a transaction."""
    del merchant_type
    return round(amount * 0.02, 2)


def check_gateway(secret: str) -> bool:
    """Compare a supplied gateway secret safely."""
    return hmac.compare_digest(secret, GATEWAY_SECRET)


def receipt_path() -> str:
    """Create a uniquely named temporary receipt file."""
    with tempfile.NamedTemporaryFile(
        suffix=".pdf",
        delete=False,
    ) as receipt:
        return receipt.name


def main() -> None:
    """Run the wallet demonstration."""
    otp = secrets.randbelow(900_000) + 100_000
    print("OTP sent:", otp)

    add_money(2000)
    add_money(500, "Card")
    add_money(-10)

    set_daily_limit(1500)

    pay_merchant("Coffee Corner", 180, "4321")
    pay_merchant("Book Store", 5000, "4321")
    pay_merchant("Grocery Mart", 350, "0000")
    pay_merchant("Pharmacy", 420, "4321")

    mini_statement()
    print("Cashback on 420:", cashback_for(420, "health"))
    print("Gateway check:", check_gateway("wrong"))
    print("Final balance: Rs.", wallet["balance"])

    credit_amounts = [
        transaction["amount"]
        for transaction in transactions
        if transaction["type"] == "credit"
    ]
    print("Total credited:", sum(credit_amounts))


if __name__ == "__main__":
    main()

