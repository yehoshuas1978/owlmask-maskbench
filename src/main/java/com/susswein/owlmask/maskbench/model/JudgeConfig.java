package com.susswein.owlmask.maskbench.model;

public record JudgeConfig(
        String name,
        String config,
        String protocol,
        String baseUrl,
        String model,
        String apiKey,
        double temperature,
        int maxOutputTokens,
        double maxRunCostUsd
) {}
