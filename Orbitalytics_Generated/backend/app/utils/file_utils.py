"""
Orbitalytics - File & Storage Utilities
"""
from pathlib import Path
import hashlib
import re

def format_bytes(size_in_bytes: int) -> str:
    """Formats bytes into human readable KB, MB, GB, TB string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(size_in_bytes) < 1024.0:
            return f"{size_in_bytes:3.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} PB"

def get_directory_size_bytes(directory_path: Path) -> int:
    """Calculates total size in bytes of all files in directory recursively."""
    if not directory_path.exists():
        return 0
    total = 0
    for entry in directory_path.rglob('*'):
        if entry.is_file():
            total += entry.stat().st_size
    return total

def sanitize_filename(name: str) -> str:
    """Removes unsafe characters for file system saving."""
    return re.sub(r'[^a-zA-Z0-9_\-\.]', '_', name)

def compute_sha256(file_path: Path) -> str:
    """Computes SHA256 checksum for data integrity validation."""
    if not file_path.exists():
        return ""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
