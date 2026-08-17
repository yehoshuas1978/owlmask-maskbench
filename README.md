# owlmask-maskbench — RETIRED 2026-08-16

> **This repository is an archive. Nothing here is built, tested, or called.**
> Do not add code to it. Do not read its corpus as current.

## Where the live things went

| What | Now lives at |
|---|---|
| The six-language corpus (`texts-to-mask-*`) | `owlmask-sdk/corpus/` |
| `scripts/generate_raw_data.py` | `owlmask-sdk/tools/corpus/generate_raw_data.py` |
| `scripts/repair_manifests.py` | `owlmask-sdk/tools/corpus/repair_manifests.py` |
| The masking acceptance gate | `owlmask-sdk/tests/masking_api/test_maskbench_acceptance.py` |
| The judged certification lane | `owlmask-sdk/tools/scenario_validation/maskbench_scan.py` |

**The copies under `data/` and `scripts/` in this repo are frozen duplicates.**
They were correct at commit `e7e2897` and will not be updated again. Edit the
`owlmask-sdk` copies; a change made here reaches nothing.

## Why the Java CLI was retired

The CLI (`benchmark-pairs`, `judge-pairs`, `explain`) was deleted on 2026-08-16
after an audit found it had **zero callers anywhere in the workspace**:

- not a module in the root reactor `pom.xml`
- no Maven dependency on the `owlmask-maskbench` artifact
- no Java code in `owlmask-code`, `owlmask-llm`, `owlmask-share`, or
  `owltable-app` referencing its classes
- no CI outside this repo built or ran it; its own `verify.yml` only tested itself
- `judge-pairs`, the LLM lane and its whole reason to exist, was never wired —
  it refused with exit 2

It was a second implementation, in a second language, of judging that
`owlmask-sdk` already does in Python — and the Python lane is the one that
produced every certification result on record. Keeping a fixed-but-uncalled
judge in the tree is a hazard: the next reader assumes it is the certification
path. It is not, and never was.

Deeper history, including the 2026-08-03 repair of `judge-pairs` (which had been
writing a hardcoded `{"pass":1,"fail":0}` **without reading its input**), is in
`owlmask-share/documentation/plan/improvements/owlmask-maskbench.md`. **Discard
any maskbench report produced before 2026-08-03.**

## What this repo is still good for

Its git history is the only record of how the corpus was built and repaired. In
particular `data/manifests-pre-x12-backup/` and `data/manifests-repaired-x12/`
are the before/after of the X-12 manifest repair, cited by
`FREETEXT_MASKING_FIX_LEDGER.md` and `LANGUAGE_SUPPORT_RUN_HISTORY.md`. Those two
directories were **not** carried into `owlmask-sdk`, so this archive is the only
place they exist.

Full contents remain recoverable at any time:

```bash
git clone https://github.com/yehoshuas1978/owlmask-maskbench.git
```

The Java sources are in the history at `e7e2897`; recover with
`git show e7e2897:pom.xml` or `git checkout e7e2897 -- src/`.
