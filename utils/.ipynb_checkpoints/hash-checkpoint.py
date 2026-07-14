from hashlib import sha256
from pathlib import Path

def file_hash(path: str | Path) -> str:
    """Return the SHA-256 hash of a file."""

    return sha256(
        Path(path).read_bytes()
    ).hexdigest()