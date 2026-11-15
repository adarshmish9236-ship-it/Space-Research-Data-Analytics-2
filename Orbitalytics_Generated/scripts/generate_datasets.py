"""
Orbitalytics - Standalone Dataset Generation Script
"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.services.data_generator import generate_all_datasets

if __name__ == "__main__":
    profile = sys.argv[1] if len(sys.argv) > 1 else "medium"
    generate_all_datasets(profile=profile)

