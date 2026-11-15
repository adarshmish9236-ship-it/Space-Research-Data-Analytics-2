import os

large_files = []
for root, dirs, files in os.walk('.'):
    # skip .git if exists
    if '.git' in root:
        continue
    for f in files:
        path = os.path.join(root, f)
        try:
            sz = os.path.getsize(path)
            if sz > 10 * 1024 * 1024: # > 10MB
                large_files.append((path, sz / (1024 * 1024)))
        except Exception:
            pass

print(f"Total files > 10MB: {len(large_files)}")
for p, s in sorted(large_files, key=lambda x: x[1], reverse=True):
    print(f"  {p}: {s:.2f} MB")
