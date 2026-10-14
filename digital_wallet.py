
"""Demonstration wallet for the static code analysis lab."""

import hashlib
import hmac
import os
import secrets
import tempfile
from datetime import datetime

GATEWAY_SECRET = os.getenv("GATEWAY_SECRET")
WALLET_PIN = os.getenv("WALLET_PIN", "4321")
wallet = {"balance": 0.0}
daily_limit = 1000
transactions = []


def hashPin(pin):
    """Hash a PIN using PBKDF2-HMAC-SHA256."""
    return hashlib.pbkdf2_hmac(
        "sha256", pin.encode(), b"wallet-demo-salt", 100_000
    )


def addMoney(amount, source="UPI", log=None):
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


def setDailyLimit(newLimit):
    """Set the daily payment limit."""
    global daily_limit
    daily_limit = newLimit


def payMerchant(merchant, amount, pin):
    """Validate the PIN and pay a merchant if permitted."""
    if not hmac.compare_digest(hashPin(pin), hashPin(WALLET_PIN)):
        print("Wrong PIN for payment to", merchant)
        return False
    if amount <= 0 or amount > wallet["balance"] or amount > daily_limit:
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


def miniStatement(count=3):
    """Print the most recent transactions."""
    if count <= 0:
        return
    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashbackFor(amount, merchantType):
    """Calculate cashback at two percent."""
    return round(amount * 0.02, 2)


def checkGateway(secret):
    """Compare a key with the configured gateway secret."""
    if not GATEWAY_SECRET or not secret:
        return False
    return hmac.compare_digest(secret, GATEWAY_SECRET)


def receiptPath():
    """Create a securely generated temporary PDF filename."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as file:
        return file.name


def main():
    """Run the wallet demonstration."""
    otp = secrets.randbelow(900_000) + 100_000
    print("OTP sent:", otp)
    addMoney(2000)
    addMoney(500, "Card")
    addMoney(-10)
    setDailyLimit(1500)
    payMerchant("Coffee Corner", 180, "4321")
    payMerchant("Book Store", 5000, "4321")
    payMerchant("Grocery Mart", 350, "0000")
    payMerchant("Pharmacy", 420, "4321")
    miniStatement()
    print("Cashback on 420:", cashbackFor(420, "health"))
    print("Gateway check:", checkGateway("wrong"))
    print("Final balance: Rs.", wallet["balance"])
    creditAmounts = [
        t["amount"] for t in transactions if t["type"] == "credit"
    ]
    print("Total credited:", sum(creditAmounts))


if __name__ == "__main__":
    main()

