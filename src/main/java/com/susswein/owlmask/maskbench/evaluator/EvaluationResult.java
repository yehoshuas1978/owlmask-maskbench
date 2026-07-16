package com.susswein.owlmask.maskbench.evaluator;

import java.util.Map;

public record EvaluationResult(
    boolean passed,
    String reason,
    Map<String, Object> metrics
) {}
