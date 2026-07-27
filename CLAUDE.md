# OwlMask MaskBench Instructions

The workspace-wide product and engineering instructions are in
[`../CLAUDE.md`](../CLAUDE.md). This file adds rules specific to
`owlmask-maskbench`.

## Scope

`owlmask-maskbench` is a standalone Java 21 CLI that judges supplied
original/masked text pairs using deterministic evaluation plus an optional LLM
review cascade. It is the intended **acceptance layer** for the masking engine —
the thing that says whether a language profile is good enough to certify.

It is a measurement tool. Its output becomes a compliance claim, so a bug here
does not crash anything; it produces a confident wrong number.

## Technology

Derive versions from `pom.xml`. Ships the family's only Maven wrapper — use
`./mvnw`.

## Rules that are easy to get wrong

- **Run judge and benchmark rounds SERIALLY.** Concurrency-2 thrashes the
  available cores and produces a net slowdown, not throughput.
- **Never `SIGSTOP` a running judge.** The wrapper treats a stop as an exit and
  kills the run. Let it finish or terminate it properly.
- **The judge writes its output only at the end.** A long run that is interrupted
  produces nothing; budget for the full duration.
- **A leak rule must not be re-implemented here.** `value_leaked()` in
  `tools/scenario_validation/maskbench_scan.py` (owlmask-sdk) and
  `masking_shared/masker/residual.py` already disagree about what counts as a
  surviving fragment. The certification gate and the runtime scanner must apply
  the *same* definition, or a profile can certify under one rule and abstain
  under another in production.
- **LLM-review mode must record model, temperature and prompt version** in the
  report, or two runs cannot be compared and the number means nothing.

## Verification

```bash
./mvnw verify
```

When changing scoring, re-run an existing dataset and **report the changed
numbers explicitly** rather than accepting them — a scoring change silently
moves every historical comparison.
