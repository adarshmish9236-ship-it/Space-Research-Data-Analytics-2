#!/bin/bash
# Pig execution wrapper - sets environment variables correctly
export PIG_HOME=/opt/pig-0.17.0
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/opt/hadoop-3.2.1
export HADOOP_CONF_DIR=/opt/hadoop-3.2.1/etc/hadoop
export PATH=$PATH:/opt/pig-0.17.0/bin:/opt/hadoop-3.2.1/bin
export PIG_CLASSPATH=$HADOOP_CONF_DIR

# Test pig version
pig -version
echo "PIG_ENV_OK"

