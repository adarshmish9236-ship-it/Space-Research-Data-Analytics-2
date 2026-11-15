"""
Remove old Cesium orbit engine block from index.html.
Lines 5663 through 6161 (1-indexed) are the old duplicate Cesium functions.
"""
path = "frontend/index.html"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

total = len(lines)
print(f"Total lines before: {total}")

# Delete lines 5663 to 6161 inclusive (convert to 0-indexed: 5662 to 6160)
del lines[5662:6161]

print(f"Total lines after:  {len(lines)}")

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Done.")
