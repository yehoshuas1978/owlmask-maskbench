# owlmask-maskbench

Standalone Java 21 command-line application that judges supplied original/masked text pairs using deterministic evaluation and optional LLM review.

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

Judge cascade configuration lives under [`config/`](config/) and sample
datasets under [`data/`](data/).

## Documentation

Usage examples and judge configuration are documented in the OwlMask hub
(links resolve in the workspace checkout):

- [MaskBench examples](../owlmask-share/documentation/current/maskbench/EXAMPLES.md)
- [Judge configuration](../owlmask-share/documentation/current/maskbench/JUDGE_CONFIG.md)
