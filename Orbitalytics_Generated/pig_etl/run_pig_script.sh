#!/bin/bash
# =============================================================================
# run_pig_script.sh — Robust Pig Latin execution wrapper
# Usage: /tmp/pig_etl/run_pig_script.sh <pig_script_path>
# Automatically cleans existing target HDFS directories before execution.
# =============================================================================

export PIG_HOME=/opt/pig-0.17.0
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/opt/hadoop-3.2.1
export HADOOP_CONF_DIR=/opt/hadoop-3.2.1/etc/hadoop
export PATH=/opt/pig-0.17.0/bin:/opt/hadoop-3.2.1/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export PIG_CLASSPATH=$HADOOP_CONF_DIR

SCRIPT=$1
if [ -z "$SCRIPT" ] || [ ! -f "$SCRIPT" ]; then
    echo "ERROR: Valid Pig script path required. Given: '$SCRIPT'"
    exit 1
fi

echo "================================================================="
echo "ORBITALYTICS PIG ETL: Executing $(basename $SCRIPT)"
echo "Timestamp: $(date)"
echo "Script Path: $SCRIPT"
echo "================================================================="

# Extract STORE paths from the script and delete if they already exist
echo "Extracting and cleaning target HDFS paths..."
STORE_PATHS=$(grep -i "INTO 'hdfs:" "$SCRIPT" | sed -e "s/.*INTO 'hdfs:\/\/namenode:9000//g" -e "s/'.*//g")

for p in $STORE_PATHS; do
    if [ -n "$p" ]; then
        echo "  Checking target: $p"
        hdfs dfs -rm -r -skipTrash "$p" 2>/dev/null
    fi
done

echo "Starting Pig MapReduce execution..."
pig -x mapreduce "$SCRIPT"
EXIT_CODE=$?

echo "================================================================="
echo "Pig execution finished with exit code: $EXIT_CODE"
echo "Timestamp: $(date)"
echo "================================================================="
exit $EXIT_CODE
