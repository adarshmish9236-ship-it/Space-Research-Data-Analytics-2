"""
ORBITALYTICS Phase 4 — Master Apache Pig ETL Orchestrator & Metric Collector
Coordinates execution of all 9 Pig Latin ETL pipelines against the live Docker Hadoop cluster.
Captures actual execution logs, job IDs, input/output counts, quarantine records, and execution durations.
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from typing import Dict, Any, List

DOMAINS = [
    {
        "id": "01",
        "name": "missions",
        "script": "01_missions_etl.pig",
        "bronze_path": "/orbitalytics/bronze/missions/space_missions.csv",
        "silver_path": "/orbitalytics/silver/pig_missions",
        "quarantine_path": "/orbitalytics/quarantine/pig_missions_rejected",
        "gold_paths": [
            "/orbitalytics/gold/pig_mission_analytics",
            "/orbitalytics/gold/pig_mission_by_year_type"
        ]
    },
    {
        "id": "02",
        "name": "satellites",
        "script": "02_satellites_etl.pig",
        "bronze_path": "/orbitalytics/bronze/satellites/satellites_orbital.csv",
        "silver_path": "/orbitalytics/silver/pig_satellites",
        "quarantine_path": "/orbitalytics/quarantine/pig_satellites_rejected",
        "gold_paths": [
            "/orbitalytics/gold/pig_satellite_analytics",
            "/orbitalytics/gold/pig_satellite_by_agency_year"
        ]
    },
    {
        "id": "03",
        "name": "launches",
        "script": "03_launches_etl.pig",
        "bronze_path": "/orbitalytics/bronze/launches/launch_activities.csv",
        "silver_path": "/orbitalytics/silver/pig_launches",
        "quarantine_path": "/orbitalytics/quarantine/pig_launches_rejected",
        "gold_paths": [
            "/orbitalytics/gold/pig_launch_analytics",
            "/orbitalytics/gold/pig_launch_outcome_rates",
            "/orbitalytics/gold/pig_launch_by_vehicle"
        ]
    },
    {
        "id": "04",
        "name": "equipment_demand",
        "script": "04_equipment_demand_etl.pig",
        "bronze_path": "/orbitalytics/bronze/equipment_demand/equipment_component_demand.csv",
        "silver_path": "/orbitalytics/silver/pig_equipment_demand",
        "quarantine_path": "/orbitalytics/quarantine/pig_equipment_demand_rejected",
        "gold_paths": [
            "/orbitalytics/gold/pig_equipment_demand_analytics",
            "/orbitalytics/gold/pig_component_demand_summary",
            "/orbitalytics/gold/pig_shortage_risk_summary"
        ]
    },
    {
        "id": "05",
        "name": "agency_expenditure",
        "script": "05_agency_expenditure_etl.pig",
        "bronze_path": "/orbitalytics/bronze/agency_expenditure/agency_research_expenditures.csv",
        "silver_path": "/orbitalytics/silver/pig_agency_expenditure",
        "quarantine_path": "/orbitalytics/quarantine/pig_agency_expenditure_rejected",
        "gold_paths": [
            "/orbitalytics/gold/pig_agency_expenditure_analytics",
            "/orbitalytics/gold/pig_expenditure_by_country"
        ]
    },
    {
        "id": "06",
        "name": "resource_consumption",
        "script": "06_resource_consumption_etl.pig",
        "bronze_path": "/orbitalytics/bronze/resource_consumption/resource_consumption.csv",
        "silver_path": "/orbitalytics/silver/pig_resource_consumption",
        "quarantine_path": "/orbitalytics/quarantine/pig_resource_consumption_rejected",
        "gold_paths": [
            "/orbitalytics/gold/pig_resource_analytics",
            "/orbitalytics/gold/pig_resource_by_agency"
        ]
    },
    {
        "id": "07",
        "name": "manufacturing",
        "script": "07_manufacturing_etl.pig",
        "bronze_path": "/orbitalytics/bronze/manufacturing/satellite_manufacturing_requirements.csv",
        "silver_path": "/orbitalytics/silver/pig_manufacturing",
        "quarantine_path": "/orbitalytics/quarantine/pig_manufacturing_rejected",
        "gold_paths": [
            "/orbitalytics/gold/pig_manufacturing_analytics",
            "/orbitalytics/gold/pig_manufacturing_by_year"
        ]
    },
    {
        "id": "08",
        "name": "infrastructure",
        "script": "08_infrastructure_etl.pig",
        "bronze_path": "/orbitalytics/bronze/infrastructure/space_infrastructure_requirements.csv",
        "silver_path": "/orbitalytics/silver/pig_infrastructure",
        "quarantine_path": "/orbitalytics/quarantine/pig_infrastructure_rejected",
        "gold_paths": [
            "/orbitalytics/gold/pig_infrastructure_analytics",
            "/orbitalytics/gold/pig_infrastructure_by_agency"
        ]
    },
    {
        "id": "09",
        "name": "research_projects",
        "script": "09_research_projects_etl.pig",
        "bronze_path": "/orbitalytics/bronze/research_projects/research_investment_future_projects.csv",
        "silver_path": "/orbitalytics/silver/pig_research_projects",
        "quarantine_path": "/orbitalytics/quarantine/pig_research_projects_rejected",
        "gold_paths": [
            "/orbitalytics/gold/pig_research_projects_analytics",
            "/orbitalytics/gold/pig_research_by_tier"
        ]
    }
]


def run_cmd(cmd: str, timeout: int = 360) -> tuple[int, str]:
    """Execute command and return (code, output)."""
    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace"
        )
        return proc.returncode, proc.stdout + proc.stderr
    except subprocess.TimeoutExpired:
        return -1, "Command timed out"
    except Exception as e:
        return -1, str(e)


def count_hdfs_lines(hdfs_path: str) -> int:
    """Count non-empty lines in an HDFS path/directory."""
    if hdfs_path.endswith(".csv"):
        cmd = f'docker exec hadoop-namenode bash -c "hdfs dfs -cat {hdfs_path} 2>/dev/null | grep -v \'^$\' | wc -l"'
    else:
        cmd = f'docker exec hadoop-namenode bash -c "hdfs dfs -cat {hdfs_path}/* 2>/dev/null | grep -v \'^$\' | wc -l"'
    code, out = run_cmd(cmd)
    if code == 0:
        for line in reversed(out.strip().split("\n")):
            line = line.strip()
            if line.isdigit():
                return int(line)
    return 0


def execute_pig_pipeline(domain: Dict[str, Any], log_dir: str) -> Dict[str, Any]:
    """Execute a single domain's Pig script and gather stats."""
    name = domain["name"]
    script = domain["script"]
    now_str = datetime.now().strftime('%H:%M:%S')
    print(f"\n[{now_str}] >>> Starting Pig ETL for domain: {name} ({script})", flush=True)
    
    # 1. Measure Bronze input count (excluding header)
    total_bronze = count_hdfs_lines(domain["bronze_path"])
    bronze_data_records = max(0, total_bronze - 1)  # subtract CSV header
    print(f"  Bronze input total lines: {total_bronze} (data rows: {bronze_data_records})", flush=True)
    
    # 2. Execute Pig script inside namenode container
    start_time = time.time()
    exec_cmd = f'docker exec hadoop-namenode bash -c "/tmp/pig_etl/run_pig_script.sh /tmp/pig_etl/{script}"'
    code, log_output = run_cmd(exec_cmd, timeout=360)
    duration = round(time.time() - start_time, 2)
    
    # Save log file
    log_file_path = os.path.join(log_dir, f"{domain['id']}_{name}_pig.log")
    with open(log_file_path, "w", encoding="utf-8") as f:
        f.write(log_output)
    
    # Extract Hadoop Job IDs and MapReduce statistics
    job_ids = []
    for line in log_output.split("\n"):
        if "HadoopJobId:" in line:
            parts = line.split("HadoopJobId:")
            if len(parts) > 1:
                job_ids.append(parts[1].strip())
    
    success = (code == 0) and ("Success!" in log_output or "100% complete" in log_output)
    
    # 3. Measure Output Counts
    silver_count = count_hdfs_lines(domain["silver_path"])
    quarantine_count = count_hdfs_lines(domain["quarantine_path"])
    
    # Gold counts
    gold_counts = {}
    for gpath in domain["gold_paths"]:
        gname = os.path.basename(gpath)
        gold_counts[gname] = count_hdfs_lines(gpath)
        
    accounted_for = silver_count + quarantine_count
    discrepancy = bronze_data_records - accounted_for
    
    status_str = "SUCCESS" if success else "FAILED"
    print(f"  Execution finished in {duration}s | Status: {status_str}", flush=True)
    print(f"  Hadoop Jobs: {', '.join(job_ids) if job_ids else 'N/A'}", flush=True)
    print(f"  Silver Output: {silver_count} rows | Quarantine: {quarantine_count} rows", flush=True)
    print(f"  Accountability: Bronze({bronze_data_records}) == Silver({silver_count}) + Quarantine({quarantine_count}) (diff: {discrepancy})", flush=True)
    print(f"  Gold Aggregations: {gold_counts}", flush=True)
    
    return {
        "domain": name,
        "script": script,
        "status": status_str,
        "duration_seconds": duration,
        "exit_code": code,
        "job_ids": job_ids,
        "bronze_input_rows": bronze_data_records,
        "silver_output_rows": silver_count,
        "quarantine_output_rows": quarantine_count,
        "total_accounted_rows": accounted_for,
        "silent_deletion_count": discrepancy,
        "gold_aggregation_counts": gold_counts,
        "log_file": log_file_path,
        "timestamp": datetime.now().isoformat()
    }


def main():
    base_dir = r"E:\PROJECTS\BDT"
    log_dir = os.path.join(base_dir, "docs", "phase_4", "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    target_domain = sys.argv[1] if len(sys.argv) > 1 else None
    
    results = []
    print("=" * 70, flush=True)
    print("ORBITALYTICS PHASE 4: APACHE PIG ETL EXECUTION SUITE", flush=True)
    print(f"Started at: {datetime.now().isoformat()}", flush=True)
    print("=" * 70, flush=True)
    
    domains_to_run = [d for d in DOMAINS if d["name"] == target_domain or d["id"] == target_domain] if target_domain else DOMAINS
    
    for domain in domains_to_run:
        res = execute_pig_pipeline(domain, log_dir)
        results.append(res)
        
    manifest_path = os.path.join(base_dir, "docs", "phase_4", "pig_etl_execution_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        
    print("\n" + "=" * 70, flush=True)
    print(f"PIG ETL EXECUTION COMPLETE — Processed {len(results)} domains", flush=True)
    print(f"Manifest saved to: {manifest_path}", flush=True)
    print("=" * 70, flush=True)


if __name__ == "__main__":
    main()
