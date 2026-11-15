#!/usr/bin/env python3
"""
ORBITALYTICS Phase 5 — MapReduce Master Orchestrator
Automates submission, monitoring, and validation of all 7 Hadoop Streaming MapReduce jobs.
Harvests live YARN application IDs, execution counters, and output metrics.
"""

import os
import sys
import json
import time
import re
import subprocess
from datetime import datetime

DOCKER_CONTAINER = "hadoop-namenode"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_PHASE5 = os.path.join(PROJECT_ROOT, "docs", "phase_5")
LOGS_DIR = os.path.join(DOCS_PHASE5, "logs")
MANIFEST_FILE = os.path.join(DOCS_PHASE5, "mapreduce_execution_manifest.json")

MAPREDUCE_JOBS = [
    {
        "id": "01",
        "name": "01_equipment_demand",
        "description": "Equipment Demand by Component with Combiner Optimization",
        "mapper": "/opt/mapreduce/mappers/01_equipment_demand_mapper.py",
        "reducer": "/opt/mapreduce/reducers/01_equipment_demand_reducer.py",
        "combiner": "/opt/mapreduce/combiners/01_equipment_demand_combiner.py",
        "input_hdfs": "/orbitalytics/silver/pig_equipment_demand",
        "output_hdfs": "/orbitalytics/gold/mr_equipment_demand_by_component",
        "num_reducers": 2
    },
    {
        "id": "02",
        "name": "02_resource_consumption",
        "description": "Resource Consumption by Year and Resource",
        "mapper": "/opt/mapreduce/mappers/02_resource_consumption_mapper.py",
        "reducer": "/opt/mapreduce/reducers/02_resource_consumption_reducer.py",
        "combiner": "NONE",
        "input_hdfs": "/orbitalytics/silver/pig_resource_consumption",
        "output_hdfs": "/orbitalytics/gold/mr_resource_consumption_by_year",
        "num_reducers": 2
    },
    {
        "id": "03",
        "name": "03_missions",
        "description": "Space Missions Intelligence by Space Agency",
        "mapper": "/opt/mapreduce/mappers/03_missions_mapper.py",
        "reducer": "/opt/mapreduce/reducers/03_missions_reducer.py",
        "combiner": "NONE",
        "input_hdfs": "/orbitalytics/silver/pig_missions",
        "output_hdfs": "/orbitalytics/gold/mr_missions_by_agency",
        "num_reducers": 2
    },
    {
        "id": "04",
        "name": "04_satellites",
        "description": "Satellite Deployment Analytics by Orbit Type",
        "mapper": "/opt/mapreduce/mappers/04_satellites_mapper.py",
        "reducer": "/opt/mapreduce/reducers/04_satellites_reducer.py",
        "combiner": "NONE",
        "input_hdfs": "/orbitalytics/silver/pig_satellites",
        "output_hdfs": "/orbitalytics/gold/mr_satellites_by_orbit_type",
        "num_reducers": 2
    },
    {
        "id": "05",
        "name": "05_launches",
        "description": "Launch Activities by Year with Associative Combiner",
        "mapper": "/opt/mapreduce/mappers/05_launches_mapper.py",
        "reducer": "/opt/mapreduce/reducers/05_launches_reducer.py",
        "combiner": "/opt/mapreduce/combiners/05_launches_combiner.py",
        "input_hdfs": "/orbitalytics/silver/pig_launches",
        "output_hdfs": "/orbitalytics/gold/mr_launches_by_year",
        "num_reducers": 2
    },
    {
        "id": "06",
        "name": "06_manufacturing",
        "description": "Manufacturing Quantity by Component Subsystem",
        "mapper": "/opt/mapreduce/mappers/06_manufacturing_mapper.py",
        "reducer": "/opt/mapreduce/reducers/06_manufacturing_reducer.py",
        "combiner": "NONE",
        "input_hdfs": "/orbitalytics/silver/pig_equipment_demand",
        "output_hdfs": "/orbitalytics/gold/mr_manufacturing_by_component",
        "num_reducers": 2
    },
    {
        "id": "07",
        "name": "07_research_investment",
        "description": "Research & Infrastructure Investment by Agency and Year",
        "mapper": "/opt/mapreduce/mappers/07_research_investment_mapper.py",
        "reducer": "/opt/mapreduce/reducers/07_research_investment_reducer.py",
        "combiner": "NONE",
        "input_hdfs": "/orbitalytics/silver/pig_agency_expenditure",
        "output_hdfs": "/orbitalytics/gold/mr_research_investment_by_agency_year",
        "num_reducers": 2
    }
]

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode, result.stdout, result.stderr

def sync_code_to_container():
    print("[INIT] Synchronizing MapReduce scripts to container...")
    run_cmd(f"docker exec {DOCKER_CONTAINER} rm -rf /opt/mapreduce")
    mapreduce_local = os.path.join(PROJECT_ROOT, "mapreduce")
    code, out, err = run_cmd(f'docker cp "{mapreduce_local}" {DOCKER_CONTAINER}:/opt/mapreduce')
    if code != 0:
        print(f"[ERROR] Failed to docker cp: {err}")
        sys.exit(1)
    run_cmd(f"docker exec {DOCKER_CONTAINER} chmod -R +x /opt/mapreduce")
    print("[INIT] Synchronization complete.")

def count_hdfs_lines(hdfs_path):
    cmd = f'docker exec {DOCKER_CONTAINER} bash -c "hdfs dfs -cat {hdfs_path}/part* 2>/dev/null | wc -l"'
    code, out, _ = run_cmd(cmd)
    if code == 0 and out.strip().isdigit():
        return int(out.strip())
    return 0

def fetch_sample_records(hdfs_path, n=3):
    cmd = f'docker exec {DOCKER_CONTAINER} bash -c "hdfs dfs -cat {hdfs_path}/part* 2>/dev/null | head -n {n}"'
    code, out, _ = run_cmd(cmd)
    if code == 0:
        lines = [line.strip() for line in out.strip().splitlines() if line.strip() and not line.startswith("2026-")]
        return lines[:n]
    return []

def execute_job(job_cfg):
    job_name = job_cfg["name"]
    print(f"\n===============================================================================")
    print(f"[ORBITALYTICS] Starting MapReduce Job {job_cfg['id']}: {job_cfg['name']}")
    print(f"  Description:  {job_cfg['description']}")
    print(f"  Input HDFS:   {job_cfg['input_hdfs']}")
    print(f"  Output HDFS:  {job_cfg['output_hdfs']}")
    print(f"  Reducers:     {job_cfg['num_reducers']}")
    print(f"===============================================================================")

    os.makedirs(LOGS_DIR, exist_ok=True)
    log_path = os.path.join(LOGS_DIR, f"{job_name}.log")

    start_time = time.time()

    docker_cmd = (
        f'docker exec {DOCKER_CONTAINER} bash /opt/mapreduce/run_mapreduce_job.sh '
        f'"{job_name}" '
        f'"{job_cfg["mapper"]}" '
        f'"{job_cfg["reducer"]}" '
        f'"{job_cfg["combiner"]}" '
        f'"{job_cfg["input_hdfs"]}" '
        f'"{job_cfg["output_hdfs"]}" '
        f'{job_cfg["num_reducers"]}'
    )

    exit_code, stdout, stderr = run_cmd(docker_cmd)
    duration = round(time.time() - start_time, 2)

    combined_log = stdout + "\n" + stderr
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(combined_log)

    status = "SUCCESS" if exit_code == 0 else "FAILED"

    # Extract YARN application and Job IDs
    app_ids = list(set(re.findall(r"application_\d+_\d+", combined_log)))
    job_ids = list(set(re.findall(r"job_\d+_\d+", combined_log)))

    # Extract Counters
    map_input_match = re.search(r"Map input records=(\d+)", combined_log)
    map_output_match = re.search(r"Map output records=(\d+)", combined_log)
    combine_input_match = re.search(r"Combine input records=(\d+)", combined_log)
    combine_output_match = re.search(r"Combine output records=(\d+)", combined_log)
    reduce_groups_match = re.search(r"Reduce input groups=(\d+)", combined_log)
    reduce_output_match = re.search(r"Reduce output records=(\d+)", combined_log)

    counters = {
        "map_input_records": int(map_input_match.group(1)) if map_input_match else None,
        "map_output_records": int(map_output_match.group(1)) if map_output_match else None,
        "combine_input_records": int(combine_input_match.group(1)) if combine_input_match else 0,
        "combine_output_records": int(combine_output_match.group(1)) if combine_output_match else 0,
        "reduce_input_groups": int(reduce_groups_match.group(1)) if reduce_groups_match else None,
        "reduce_output_records": int(reduce_output_match.group(1)) if reduce_output_match else None,
    }

    output_rows = count_hdfs_lines(job_cfg["output_hdfs"])
    sample_records = fetch_sample_records(job_cfg["output_hdfs"], 3)

    record = {
        "job_id": job_cfg["id"],
        "name": job_name,
        "description": job_cfg["description"],
        "status": status,
        "exit_code": exit_code,
        "duration_seconds": duration,
        "yarn_application_id": app_ids[0] if app_ids else None,
        "mapreduce_job_id": job_ids[0] if job_ids else None,
        "counters": counters,
        "output_hdfs_path": job_cfg["output_hdfs"],
        "output_record_count": output_rows,
        "sample_records": sample_records,
        "log_file": log_path,
        "timestamp": datetime.now().isoformat()
    }

    print(f"[{status}] Duration: {duration}s | App: {record['yarn_application_id']} | Job: {record['mapreduce_job_id']}")
    print(f"  Map In: {counters['map_input_records']} -> Map Out: {counters['map_output_records']}")
    if counters['combine_output_records']:
        print(f"  Combiner: {counters['combine_input_records']} in -> {counters['combine_output_records']} out")
    print(f"  Reduce Groups: {counters['reduce_input_groups']} -> Reduce Out: {counters['reduce_output_records']}")
    print(f"  HDFS Output Rows: {output_rows}")
    return record

def main():
    print("=" * 80)
    print("ORBITALYTICS Phase 5 — Distributed Hadoop MapReduce Execution")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    sync_code_to_container()

    manifest = []
    total_start = time.time()

    for job in MAPREDUCE_JOBS:
        rec = execute_job(job)
        manifest.append(rec)

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    total_duration = round(time.time() - total_start, 2)
    successful_jobs = sum(1 for r in manifest if r["status"] == "SUCCESS")

    print("\n" + "=" * 80)
    print("MAPREDUCE EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Total Jobs:       {len(manifest)}")
    print(f"Successful:       {successful_jobs} / {len(manifest)}")
    print(f"Total Duration:   {total_duration} seconds")
    print(f"Manifest Saved:   {MANIFEST_FILE}")
    print("=" * 80)

    if successful_jobs != len(manifest):
        sys.exit(1)

if __name__ == '__main__':
    main()
