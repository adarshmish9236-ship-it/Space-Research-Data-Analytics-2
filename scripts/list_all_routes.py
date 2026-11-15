import sys
from pathlib import Path
BACKEND_DIR = Path("backend")
sys.path.insert(0, str(BACKEND_DIR))

from app.main import app

routes = []
for r in app.routes:
    if hasattr(r, "path"):
        routes.append((r.path, getattr(r, "methods", ["GET"])))

routes.sort()
print(f"Total routes registered: {len(routes)}")
for path, methods in routes:
    print(f"{list(methods)[0]:<6} {path}")
