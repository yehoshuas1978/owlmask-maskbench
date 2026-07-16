package com.susswein.owlmask.maskbench.io;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.susswein.owlmask.maskbench.model.MaskPair;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class JsonlPairReader extends BasePairReader {
    private final ObjectMapper mapper = new ObjectMapper();

    @Override
    protected List<MaskPair> parse(String text) throws Exception {
        List<MaskPair> pairs = new ArrayList<>();
        String[] lines = text.split("\r?\n");
        for (String line : lines) {
            if (line.trim().isEmpty()) {
                continue;
            }
            if (line.getBytes(StandardCharsets.UTF_8).length > MAX_ROW_BYTES) {
                throw new IllegalArgumentException("Row exceeds max of 1 MiB");
            }
            try {
                MaskPair pair = mapper.readValue(line, MaskPair.class);
                if (pair.id() == null || pair.text() == null || pair.maskedText() == null) {
                    throw new IllegalArgumentException("Missing required columns");
                }
                pairs.add(pair);
            } catch (IllegalArgumentException e) {
                throw e;
            } catch (Exception e) {
                throw new IllegalArgumentException("Invalid JSON or missing columns: " + e.getMessage(), e);
            }
        }
        return pairs;
    }
}
