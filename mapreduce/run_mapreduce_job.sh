#!/usr/bin/env bash
# =============================================================================
# ORBITALYTICS Phase 5 — MapReduce Hadoop Streaming Job Runner
# Executes genuine distributed MapReduce streaming jobs on Apache Hadoop YARN
# =============================================================================

set -e

JOB_NAME="$1"
MAPPER_PATH="$2"
REDUCER_PATH="$3"
COMBINER_PATH="$4"
INPUT_HDFS_PATH="$5"
OUTPUT_HDFS_PATH="$6"
NUM_REDUCERS="${7:-2}"

STREAMING_JAR="/opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar"

if [ -z "$JOB_NAME" ] || [ -z "$MAPPER_PATH" ] || [ -z "$REDUCER_PATH" ] || [ -z "$INPUT_HDFS_PATH" ] || [ -z "$OUTPUT_HDFS_PATH" ]; then
    echo "Usage: $0 <job_name> <mapper_path> <reducer_path> <combiner_path_or_none> <input_hdfs> <output_hdfs> [num_reducers]"
    exit 1
fi

if [ ! -f "$STREAMING_JAR" ]; then
    echo "[ERROR] Streaming jar not found at: $STREAMING_JAR"
    exit 2
fi

MAPPER_BASENAME=$(basename "$MAPPER_PATH")
REDUCER_BASENAME=$(basename "$REDUCER_PATH")

FILES_ARG="$MAPPER_PATH,$REDUCER_PATH"
COMBINER_OPTS=()

if [ "$COMBINER_PATH" != "NONE" ] && [ -n "$COMBINER_PATH" ] && [ -f "$COMBINER_PATH" ]; then
    COMBINER_BASENAME=$(basename "$COMBINER_PATH")
    FILES_ARG="$FILES_ARG,$COMBINER_PATH"
    COMBINER_OPTS=(-combiner "$COMBINER_BASENAME")
    echo "[INFO] Enabling Combiner: $COMBINER_BASENAME"
fi

echo "============================================================================="
echo "[ORBITALYTICS MAPREDUCE] Launching Job: $JOB_NAME"
echo "  Input HDFS:   $INPUT_HDFS_PATH"
echo "  Output HDFS:  $OUTPUT_HDFS_PATH"
echo "  Mapper:       $MAPPER_BASENAME"
echo "  Reducer:      $REDUCER_BASENAME"
echo "  Reducers:     $NUM_REDUCERS"
echo "============================================================================="

# Ensure destination output path is clean
echo "[INFO] Cleaning target output path: $OUTPUT_HDFS_PATH"
hdfs dfs -rm -r -skipTrash "$OUTPUT_HDFS_PATH" 2>/dev/null || true

# Execute Hadoop Streaming with verified option ordering
hadoop jar "$STREAMING_JAR" \
    -D mapreduce.job.name="Orbitalytics_MR_${JOB_NAME}" \
    -D mapreduce.map.memory.mb=1024 \
    -D mapreduce.reduce.memory.mb=1024 \
    -files "$FILES_ARG" \
    -input "$INPUT_HDFS_PATH" \
    -output "$OUTPUT_HDFS_PATH" \
    -mapper "$MAPPER_BASENAME" \
    "${COMBINER_OPTS[@]}" \
    -reducer "$REDUCER_BASENAME" \
    -numReduceTasks "$NUM_REDUCERS"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "[SUCCESS] MapReduce Job '$JOB_NAME' completed successfully."
    echo "[INFO] Verifying output directory structure:"
    hdfs dfs -ls "$OUTPUT_HDFS_PATH"
else
    echo "[FAILED] MapReduce Job '$JOB_NAME' failed with exit code $EXIT_CODE."
    exit $EXIT_CODE
fi
