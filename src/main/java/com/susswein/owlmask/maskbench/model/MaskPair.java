package com.susswein.owlmask.maskbench.model;

import java.util.List;

public record MaskPair(
        String id,
        String locale,
        String domain,
        DataClassification dataClassification,
        String text,
        String maskedText,
        List<EntityLabel> entities,
        List<String> expectedPreserved
) {
    public MaskPair {
        if (text == null) {
            throw new IllegalArgumentException("text cannot be null");
        }
        if (maskedText == null) {
            throw new IllegalArgumentException("maskedText cannot be null");
        }
        if (entities == null) {
            entities = List.of();
        }
        if (expectedPreserved == null) {
            expectedPreserved = List.of();
        }
    }
}
