# OwlMask MaskBench Instructions — RETIRED REPOSITORY

The workspace-wide product and engineering instructions are in
[`../CLAUDE.md`](../CLAUDE.md).

## Do not work in this repository

`owlmask-maskbench` was retired on 2026-08-16. Its Java CLI was deleted (zero
callers anywhere in the workspace), and its corpus and generator were moved into
`owlmask-sdk`. There is no build, no test suite, and no CI here.

**If a task sends you here, the task is pointing at the wrong repo.** Redirect:

| If asked to… | Work in |
|---|---|
| change the masking corpus | `owlmask-sdk/corpus/` |
| change the corpus generator | `owlmask-sdk/tools/corpus/generate_raw_data.py` |
| change the acceptance gate | `owlmask-sdk/tests/masking_api/test_maskbench_acceptance.py` |
| change the judged certification lane | `owlmask-sdk/tools/scenario_validation/maskbench_scan.py` |
| add an LLM judge | `owlmask-sdk` — not a second Java implementation |

The `data/` and `scripts/` copies still present here are **frozen duplicates**
kept for provenance. Editing them changes nothing; the live copies are in
`owlmask-sdk`. If you find yourself reading a corpus record from this repo to
answer a question about current behaviour, stop — read `owlmask-sdk/corpus/`
instead, because the two can now diverge.

## Rules that outlived the code

These were learned here and still apply wherever the work now lives:

- **A leak rule must not be re-implemented.** `value_leaked()` in
  `owlmask-sdk/tools/scenario_validation/maskbench_scan.py` and
  `masking_shared/masker/residual.py` already disagree about what counts as a
  surviving fragment. The certification gate and the runtime scanner must apply
  the *same* definition, or a profile can certify under one rule and abstain
  under another in production. The acceptance gate imports the shipped rule
  precisely so it cannot certify under a laxer one.
- **Run judge and benchmark rounds SERIALLY.** Concurrency-2 thrashes the
  available cores and produces a net slowdown, not throughput.
- **LLM-review mode must record model, temperature and prompt version**, or two
  runs cannot be compared and the number means nothing.
- **A measurement tool that breaks does not crash — it produces a confident
  wrong number.** This repo's own CLI is the case study: `judge-pairs` reported
  `{"pass":1,"fail":0}` for input it never opened, including for files that did
  not exist. Discard any maskbench report from before 2026-08-03.

## Recovering anything

```bash
git clone https://github.com/yehoshuas1978/owlmask-maskbench.git
git checkout e7e2897 -- src/     # the deleted Java CLI
```
