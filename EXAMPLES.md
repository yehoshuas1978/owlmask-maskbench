# OwlMask MaskBench Examples

This document provides examples of how to use the different commands available in the `owlmask-maskbench` CLI tool.

## 1. `judge-pairs`

**Explanation:**  
Judges masked pairs using both deterministic rules and Large Language Models (LLMs). This is the primary tool for deep evaluation of masked data, utilizing a cascade of LLM prompts to determine if PII or sensitive data was successfully masked.

**Examples:**

* **Judging a CSV file and outputting reports to a specific directory:**
  ```bash
  java -jar target/owlmask-maskbench-1.0.0-SNAPSHOT.jar judge-pairs \
    --pairs=sample-data.csv \
    --format=csv \
    --report-dir=reports/csv-evaluation
  ```

* **Judging a JSONL file with a specific judges configuration:**
  ```bash
  java -jar target/owlmask-maskbench-1.0.0-SNAPSHOT.jar judge-pairs \
    --pairs=sample-data.jsonl \
    --format=jsonl \
    --judges=config/judges-cascade.json \
    --report-dir=reports/jsonl-evaluation
  ```

* **Overriding data classification for developer testing:**
  ```bash
  java -jar target/owlmask-maskbench-1.0.0-SNAPSHOT.jar judge-pairs \
    --pairs=sample-data.csv \
    --format=csv \
    --assume-data-classification=PUBLIC \
    --report-dir=reports/dev-test
  ```

---

## 2. `benchmark-pairs`

**Explanation:**  
Benchmarks masked pairs using *only* deterministic rules. This command skips the LLM evaluation cascade, making it much faster and useful for quick structural checks or exact-match validations where an LLM is not required.

**Examples:**

* **Benchmarking a CSV file:**
  ```bash
  java -jar target/owlmask-maskbench-1.0.0-SNAPSHOT.jar benchmark-pairs \
    --pairs=sample-data.csv \
    --format=csv \
    --report-dir=reports/benchmark-csv
  ```

* **Benchmarking a JSONL file:**
  ```bash
  java -jar target/owlmask-maskbench-1.0.0-SNAPSHOT.jar benchmark-pairs \
    --pairs=sample-data.jsonl \
    --format=jsonl
  ```

---

## 3. `explain`

**Explanation:**  
Shows explanations and examples for all available commands directly in the terminal.

**Example:**
```bash
java -jar target/owlmask-maskbench-1.0.0-SNAPSHOT.jar explain
```
