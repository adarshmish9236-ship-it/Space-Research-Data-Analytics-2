# Orbitalytics Phase 1: Data Collection & Staging Methodology

## 1. Principles of Authentic Data Collection
The collection of space research data in Orbitalytics follows four foundational principles:
1. **Legality & Authorization:** Data is harvested exclusively from public domain, open-access, or officially published government repositories (NASA, ESA, ISRO, UNOOSA). No restricted portals or paywalled services were scraped.
2. **Provenance Preservation:** Every collected raw file is archived in `datasets/raw/public/` in its unmodified state with accompanying metadata in `datasets/metadata/public_data_source_register.json`.
3. **Data Immutability:** Raw ingested files are treated as read-only write-once data. Transformations are applied in separate staging and validated directories.
4. **Honest Attribution:** Authentic historical missions are clearly credited to their original institutional publishers.

---

## 2. Ingestion & Staging Architecture

```
[External Data Sources]
   ├── NASA Open Data Portal (data.nasa.gov)
   ├── ESA Science Exploration Archives
   ├── ISRO Official Mission Manifests
   └── Synthetic Physics-Informed Generator
               │
               ▼
   [datasets/raw/]
      ├── raw/public/     <-- Authentic NASA/ESA/ISRO mission baselines
      ├── raw/synthetic/  <-- Seeded, high-volume scalable records
      └── raw/existing/   <-- Preserved legacy project files
               │
               ▼
   [scripts/data_validation/run_validation_pipeline.py]
      ├── 1. DataStandardizer (Dates to YYYY-MM-DD, Agencies to AGY-XXX, snake_case)
      ├── 2. DataValidator (Completeness, Uniqueness, Non-negative, Allowed Domains)
      └── 3. RelationshipValidator (Foreign key cross checks)
               │
               ├────────────────────────────┐
               ▼                            ▼
   [datasets/validated/]        [datasets/rejected/]
   (Clean certified datasets)   (Quarantined defects + reasons)
```

---

## 3. Standardization Rules Applied
During the staging-to-validation transformation:
1. **Date Fields:**
   - Any raw timestamps (e.g. `2024/04/18`, `18-04-2024`, `2024-04-18T14:30:00Z`) are parsed into ISO-8601 calendar dates (`YYYY-MM-DD`).
2. **Agency Standardization:**
   - Agency strings with legacy parentheticals (e.g. `NASA (USA)`, `ISRO (India)`, `Commercial (SpaceX, etc.)`) are cross-matched against `datasets/reference/agencies/agencies.csv` and assigned canonical identifiers (`AGY-001` through `AGY-007`).
3. **Column Normalization:**
   - All column headers are converted to clean, database-safe `snake_case`.
4. **Units Separation:**
   - Text units embedded within numeric cells are stripped, with physical dimensions retained in explicit `unit_of_measure` columns.

