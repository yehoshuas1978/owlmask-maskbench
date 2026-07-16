# Judges Cascade Configuration Guide

When running the `judge-pairs` command, you can supply a JSON configuration file via the `--judges` argument (e.g., `--judges=config/judges-cascade.json`). This file defines the LLMs to use, their order of execution, and the rules for the evaluation cascade.

Here is a detailed explanation of the keys available in the configuration file.

---

## Root Level Keys (`JudgeRunConfig`)

These keys control the overall behavior of the evaluation cascade.

| Key | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| **`judges`** | Array | A list of judge configurations (see below). The order in the array determines the cascade execution order. The first judge runs first; subsequent judges only run if triggered by the `failurePolicy` or other cascade rules. | `[ { ... }, { ... } ]` |
| **`failurePolicy`** | String | The rule that determines how the cascade proceeds or fails based on individual judge results. For example, `FAIL_ON_ANY_FLAG` means if any judge flags the data, the entire evaluation is marked as failed. | `"FAIL_ON_ANY_FLAG"` |
| **`requireIndependentFamilies`** | Boolean | If `true`, enforces that multiple judges in the cascade come from independent model families (e.g., OpenAI vs Anthropic) to avoid shared blind spots. | `true` |

---

## Judge Object Keys (`JudgeConfig`)

Each object inside the `judges` array represents a single LLM configuration.

| Key | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| **`name`** | String | A human-readable identifier for this judge. Useful for logging and identifying which judge failed or passed. | `"fast-judge"` |
| **`config`** | String | The type of judge or configuration preset. Often used by the code to determine which provider implementation to load (e.g., `"openai-compatible"`). | `"openai-compatible"` |
| **`protocol`** | String | The protocol used to communicate with the LLM API. | `"https"` |
| **`baseUrl`** | String | The base URL for the LLM provider's API. | `"api.openai.com/v1"` |
| **`model`** | String | The specific model identifier to use for evaluation. | `"gpt-4o-mini"` |
| **`apiKey`** | String | The API key required to authenticate with the provider. Environment variables can often be referenced (e.g., `${OPENAI_API_KEY}`). | `"${OPENAI_API_KEY}"` |
| **`temperature`** | Number | The sampling temperature. For evaluation and deterministic outputs, this should typically be set very low (e.g., `0.0`). | `0.0` |
| **`maxOutputTokens`** | Integer | The maximum number of tokens the model is allowed to generate in its response. | `2048` |
| **`maxRunCostUsd`** | Number | A safety limit on the maximum cost in USD this judge is permitted to consume per run. Helps prevent accidental runaway costs. | `5.0` |

---

## Example Configuration

```json
{
  "failurePolicy": "FAIL_ON_ANY_FLAG",
  "requireIndependentFamilies": true,
  "judges": [
    {
      "name": "fast-judge",
      "config": "openai-compatible",
      "protocol": "https",
      "baseUrl": "api.openai.com/v1",
      "model": "gpt-4o-mini",
      "apiKey": "${OPENAI_API_KEY}",
      "temperature": 0.0,
      "maxOutputTokens": 2048,
      "maxRunCostUsd": 5.0
    },
    {
      "name": "deep-judge",
      "config": "openai-compatible",
      "protocol": "https",
      "baseUrl": "api.anthropic.com/v1",
      "model": "claude-3-5-sonnet-20240620",
      "apiKey": "${ANTHROPIC_API_KEY}",
      "temperature": 0.0,
      "maxOutputTokens": 4096,
      "maxRunCostUsd": 20.0
    }
  ]
}
```
