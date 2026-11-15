"""
Orbitalytics - Initialization Script
Prepares data lakehouse directories and executes initial dataset generation and Parquet curation.
"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.services.data_generator import generate_all_datasets
from app.services.ingestion_service import IngestionService

def init():
    print("Initializing Orbitalytics Big Data Platform...")
    generate_all_datasets(profile="medium")
    ingest = IngestionService()
    ingest.run_full_ingestion_and_curation()
    print("Initialization complete! Ready for platform launch.")

if __name__ == "__main__":
    init()

