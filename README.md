# owlmask-maskbench

Standalone Java 21 command-line application that judges supplied original/masked
text pairs using deterministic evaluation and (eventually) an LLM review cascade.

## Status — read before trusting a report

| Command | State |
|---|---|
| `benchmark-pairs` | **Working.** Reads the pairs file, evaluates every pair, writes real counts, and exits non-zero on failures. |
| `judge-pairs` | **Not wired.** Refuses with exit 2. Until 2026-08-03 it wrote a hardcoded `{"pass":1,"fail":0}` report *without reading its input* — discard any report an earlier build produced. |
| `explain` | Working (prints command help). |

The LLM judge lane used by the actual language-certification runs lives in
`owlmask-sdk` (`tools/scenario_validation/` plus the Claude/Gemini judges), not
here.

## Building

```bash
./mvnw clean verify
```

## Running

```bash
java -jar target/owlmask-maskbench-1.0.0-SNAPSHOT.jar --help
# or, after building:
./run-maskbench.sh --help
```

### End-to-end example

Against the bundled sample dataset:

```console
$ java -jar target/owlmask-maskbench-1.0.0-SNAPSHOT.jar benchmark-pairs \
    --pairs data/example-dataset.jsonl --format jsonl --report-dir build/reports
benchmark-pairs: 10 pair(s), 10 passed, 0 failed
NOTE: no pair carried `entities` spans, so leak detection did not run. Only
`expectedPreserved` was checked — a passing result here is NOT evidence that
nothing leaked.
Reports written to build/reports
$ echo $?
0
```

**Read that NOTE.** `data/example-dataset.jsonl` carries only `expectedPreserved`,
so this run proves that masking did not destroy the phrases that had to survive —
it proves nothing about whether PII leaked. Leak detection needs `entities`
spans.

With spans, the evaluator has something to look for:

```console
$ cat pairs.jsonl
{"id":"leak-spans","locale":"en-US","domain":"insurance","dataClassification":"synthetic",
 "text":"Claim for John Smith.","maskedText":"Claim for John Smith.",
 "entities":[{"entityType":"PERSON","start":10,"end":20}],"expectedPreserved":[]}
{"id":"clean-spans","locale":"en-US","domain":"insurance","dataClassification":"synthetic",
 "text":"Claim for John Smith.","maskedText":"Claim for [PERSON].",
 "entities":[{"entityType":"PERSON","start":10,"end":20}],"expectedPreserved":["Claim for"]}

$ java -jar target/owlmask-maskbench-1.0.0-SNAPSHOT.jar benchmark-pairs \
    --pairs pairs.jsonl --format jsonl --report-dir build/reports
FAIL leak-spans: Entity 'John Smith' was not fully removed
benchmark-pairs: 2 pair(s), 1 passed, 1 failed
Reports written to build/reports
$ echo $?
1
```

Failure detail goes to **stderr** and carries the pair id plus the value that
survived; the report files under `--report-dir` carry counts only, so a report
can be attached to a ticket without leaking the value that failed to mask.

### Exit codes

| Code | Meaning |
|---|---|
| `0` | Every pair passed |
| `1` | The run completed and found failing pairs — use this as the CI gate |
| `2` | The run could not happen: bad `--format`, unreadable `--pairs`, malformed rows, or an empty pairs file |

An empty or unreadable input is **exit 2 with no report written**, never a clean
pass.

### Input format

One JSON object per line (`--format jsonl`) or a CSV with the same columns
(`--format csv`):

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Unique within the file; duplicates are rejected |
| `text` | yes | The original text |
| `maskedText` | yes | The masking output being judged |
| `entities` | no | `{entityType, start, end, riskClass}` spans into `text`. **Leak detection runs only on pairs that have these.** |
| `expectedPreserved` | no | Substrings that must survive masking (clinical terms, legal boilerplate) |
| `locale`, `domain`, `dataClassification` | no | Metadata |

Limits: 10 MiB total, 1 MiB per row, 10,000 pairs, strict UTF-8.

## Layout

- [`config/`](config/) — judge cascade configuration
- [`data/`](data/) — sample dataset plus the `texts-to-mask-{en,he,de,es,fr,it}`
  certification corpora (10,000 records each). `owlmask-sdk`'s LS-05 acceptance
  gate pins a stratified slice of these; see that repo's
  `scripts/refresh_maskbench_slice.py`.

## Documentation

Usage examples and judge configuration are documented in the OwlMask hub
(links resolve in the workspace checkout):

- [MaskBench examples](../owlmask-share/documentation/current/maskbench/EXAMPLES.md)
- [Judge configuration](../owlmask-share/documentation/current/maskbench/JUDGE_CONFIG.md)
