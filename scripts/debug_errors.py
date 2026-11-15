import sys
import traceback
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.services.analytics_service import AnalyticsService
a = AnalyticsService()

print("Testing get_automated_insights():")
try:
    res = a.get_automated_insights()
    print("SUCCESS:", res)
except Exception as e:
    print("ERROR:")
    traceback.print_exc()

print("\nTesting missions analytics:")
try:
    from app.api.v1.analytics import get_missions_analytics
    res2 = get_missions_analytics()
    print("SUCCESS:", res2)
except Exception as e:
    print("ERROR:")
    traceback.print_exc()
