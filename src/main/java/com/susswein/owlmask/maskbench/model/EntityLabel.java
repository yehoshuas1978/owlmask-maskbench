package com.susswein.owlmask.maskbench.model;

public record EntityLabel(
        int start,
        int end,
        String entityType,
        String riskClass
) {}
