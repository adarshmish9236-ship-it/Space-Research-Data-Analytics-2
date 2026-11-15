import sys
from pathlib import Path
sys.path.insert(0, str(Path("E:/PROJECTS/BDT")))
sys.path.insert(0, str(Path("E:/PROJECTS/BDT/backend")))

from backend.app.main import app

routes = []
for r in app.routes:
    methods = ",".join(r.methods) if hasattr(r, "methods") else "ALL"
    routes.append(f"{methods:10} {r.path}")

print(f"Total routes in FastAPI app: {len(routes)}")
for r in sorted(routes):
    print("  ", r)
