package com.susswein.owlmask.maskbench.model;

/**
 * One judge's answer, plus what produced it.
 *
 * <p>The provenance fields exist because an LLM verdict is not reproducible from
 * its text alone. A judged certification run is evidence about masking quality,
 * and evidence you cannot attribute to a specific model, temperature and prompt
 * is evidence you cannot defend or re-run. Before 2026-07-28 this record carried
 * only the content and the token counts, so a stored verdict could not say which
 * model produced it — and swapping the judge model silently changed the numbers.
 *
 * @param model         provider model id actually used for this call
 * @param temperature   sampling temperature actually sent
 * @param promptVersion identity of the prompt template that produced the verdict
 */
public record JudgeResult(
    String content,
    int promptTokens,
    int completionTokens,
    String model,
    Double temperature,
    String promptVersion
) {
    /** Backwards-compatible constructor for callers written before provenance. */
    public JudgeResult(String content, int promptTokens, int completionTokens) {
        this(content, promptTokens, completionTokens, null, null, null);
    }

    /** True when this verdict can be attributed to a specific judge configuration. */
    public boolean isAttributable() {
        return model != null && !model.isBlank() && temperature != null;
    }
}
