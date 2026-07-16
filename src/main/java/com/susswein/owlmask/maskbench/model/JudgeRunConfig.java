package com.susswein.owlmask.maskbench.model;

import java.util.List;

public record JudgeRunConfig(
        List<JudgeConfig> judges,
        String failurePolicy,
        boolean requireIndependentFamilies
) {}
