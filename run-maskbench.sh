#!/bin/bash
# Wrapper script to run owlmask-maskbench

JAR_FILE="target/owlmask-maskbench-1.0.0-SNAPSHOT.jar"

if [ ! -f "$JAR_FILE" ]; then
    echo "Error: $JAR_FILE not found."
    echo "Please build the project first using 'mvn clean install' or 'mvn package'."
    exit 1
fi

java -jar "$JAR_FILE" "$@"
