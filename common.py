"""Shared helpers for the GIT admin area: password handling and reading contacts.txt."""
import csv, hashlib, hmac, json, os, secrets

DIR = os.path.dirname(os.path.abspath(__file__))
CRED_FILE = os.path.join(DIR, "credentials.json")
CONTACTS_FILE = os.path.join(os.path.dirname(DIR), "contacts.txt")
ITERATIONS = 200_000


def _hash(password, salt, iterations):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)


def set_password(user, password):
    salt = secrets.token_bytes(16)
    data = {"user": user, "iterations": ITERATIONS, "salt": salt.hex(),
            "hash": _hash(password, salt, ITERATIONS).hex()}
    with open(CRED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)
    try:
        os.chmod(CRED_FILE, 0o600)
    except OSError:
        pass


def verify(user, password):
    """True only if user and password match the stored (salted, hashed) credentials."""
    try:
        with open(CRED_FILE, encoding="utf-8") as f:
            c = json.load(f)
        expected = bytes.fromhex(c["hash"])
        actual = _hash(password, bytes.fromhex(c["salt"]), int(c["iterations"]))
        return hmac.compare_digest(user, c["user"]) & hmac.compare_digest(actual, expected)
    except (OSError, KeyError, ValueError):
        return False


def load_contacts():
    """Return a list of dicts (newest first). Empty list if nobody has written yet."""
    if not os.path.exists(CONTACTS_FILE):
        return []
    with open(CONTACTS_FILE, newline="", encoding="utf-8") as f:
        return list(reversed(list(csv.DictReader(f))))
