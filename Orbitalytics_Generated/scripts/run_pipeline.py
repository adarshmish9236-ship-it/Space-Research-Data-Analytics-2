"""
Orbitalytics - Pipeline Execution Script
"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from app.services.pipeline_service import PipelineService

if __name__ == "__main__":
    service = PipelineService()
    res = service.trigger_full_pipeline(profile="medium")
    print(f"Pipeline finished with status: {res['status']} in {res['total_duration_sec']}s")

