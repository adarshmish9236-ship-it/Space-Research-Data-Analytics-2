"""
Orbitalytics - Pipeline & Hadoop Tests
"""
from app.services.hdfs_service import HDFSService
from app.services.hive_service import HiveService
from app.services.mapreduce_service import MapReduceService

def test_hdfs_overview():
    hdfs = HDFSService()
    ov = hdfs.get_cluster_overview()
    assert ov["total_files"] > 0
    assert ov["simulated_hdfs_blocks"] > 0
    assert len(ov["zones"]) == 6

def test_hive_analytical_query():
    hive = HiveService()
    res = hive.execute_analytical_query("agency_missions")
    assert res["rows_returned"] > 0
    assert "agency" in res["columns"]

def test_mapreduce_job():
    mr = MapReduceService()
    res = mr.run_job("missions_aggregation")
    assert res["status"] == "SUCCEEDED"
    assert res["map_input_records"] > 0
    assert len(res["records"]) > 0

