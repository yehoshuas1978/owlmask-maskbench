package com.susswein.owlmask.maskbench.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;

public enum DataClassification {
    SYNTHETIC("synthetic"),
    PUBLIC("public"),
    SANITIZED("sanitized"),
    CUSTOMER("customer"),
    PRODUCTION("production"),
    INCIDENT("incident"),
    UNKNOWN("unknown");

    private final String value;

    DataClassification(String value) {
        this.value = value;
    }

    @JsonValue
    public String getValue() {
        return value;
    }

    @JsonCreator
    public static DataClassification fromValue(String text) {
        for (DataClassification b : DataClassification.values()) {
            if (String.valueOf(b.value).equals(text)) {
                return b;
            }
        }
        return UNKNOWN;
    }
}
