package com.susswein.owlmask.maskbench.model;

public record JudgeResult(
    String content,
    int promptTokens,
    int completionTokens
) {}
