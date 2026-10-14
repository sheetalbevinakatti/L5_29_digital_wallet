"""Demonstration wallet for the static code analysis lab."""

import hashlib
import hmac
import os
import secrets
import tempfile
from datetime import datetime

GATEWAY_SECRET = os.getenv("GATEWAY_SECRET")
WALLET_PIN = os.getenv("WALLET_PIN", "4321")
DAILY_LIMIT = 1000
wallet = {"balance": 0.0}
transactions = []


def hash_pin(pin):
    """Hash a PIN using PBKDF2-HMAC-SHA256."""
    return hashlib.pbkdf2_hmac(
        "sha256", pin.encode(), b"wallet-demo-salt", 100_000
    )


def add_money(amount, source="UPI", log=None):
    """Add money to the wallet and record the credit."""
    if amount <= 0:
        return False

    if log is None:
        log = []

    wallet["balance"] += amount
    transactions.append({
        "type": "credit",
        "amount": amount,
        "party": source,
        "time": datetime.now().isoformat(),
    })
    log.append(amount)
    return True


def set_daily_limit(new_limit):
    """Set and return the daily payment limit."""
    if new_limit <= 0:
        raise ValueError("Daily limit must be positive")
    return new_limit


def pay_merchant(merchant, amount, pin, daily_limit):
    """Validate the PIN and pay a merchant if permitted."""
    if not hmac.compare_digest(hash_pin(pin), hash_pin(WALLET_PIN)):
        print("Wrong PIN for payment to", merchant)
        return False

    if (
        amount <= 0
        or amount > wallet["balance"]
        or amount > daily_limit
    ):
        print("Payment to", merchant, "declined")
        return False

    wallet["balance"] -= amount
    transactions.append({
        "type": "debit",
        "amount": amount,
        "party": merchant,
        "time": datetime.now().isoformat(),
    })
    return True


def mini_statement(count=3):
    """Print the most recent transactions."""
    if count <= 0:
        return

    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashback_for(amount, merchant_type=None):
    """Calculate cashback at two percent."""
    del merchant_type
    return round(amount * 0.02, 2)


def check_gateway(secret):
    """Compare a key with the configured gateway secret."""
    if not GATEWAY_SECRET or not secret:
        return False
    return hmac.compare_digest(secret, GATEWAY_SECRET)


def receipt_path():
    """Create a securely generated temporary PDF filename."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as file:
        return file.name


def main():
    """Run the wallet demonstration."""
    otp = secrets.randbelow(900_000) + 100_000
    print("OTP sent:", otp)

    add_money(2000)
    add_money(500, "Card")
    add_money(-10)

    daily_limit = set_daily_limit(1500)

    pay_merchant("Coffee Corner", 180, "4321", daily_limit)
    pay_merchant("Book Store", 5000, "4321", daily_limit)
    pay_merchant("Grocery Mart", 350, "0000", daily_limit)
    pay_merchant("Pharmacy", 420, "4321", daily_limit)

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
