package com.susswein.owlmask.maskbench.io;

import com.susswein.owlmask.maskbench.model.MaskPair;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class BasePairReaderTest {

    private static MaskPair pair(String id) {
        return new MaskPair(id, null, null, null, "text", "***", null, null);
    }

    /** Parses one pair per non-blank line, using the line as the pair ID. */
    private static class LinePerPairReader extends BasePairReader {
        @Override
        protected List<MaskPair> parse(String text) {
            List<MaskPair> pairs = new ArrayList<>();
            for (String line : text.split("\n")) {
                if (!line.isBlank()) {
                    pairs.add(pair(line.trim()));
                }
            }
            return pairs;
        }
    }

    private final LinePerPairReader reader = new LinePerPairReader();

    @Test
    void testTotalSizeLimitEnforced() {
        byte[] tooBig = new byte[10 * 1024 * 1024 + 1];
        Arrays.fill(tooBig, (byte) '\n');
        IllegalArgumentException e = assertThrows(IllegalArgumentException.class, () ->
            reader.read(new ByteArrayInputStream(tooBig))
        );
        assertTrue(e.getMessage().contains("10 MiB"));
    }

    @Test
    void testRowSizeLimitEnforced() {
        byte[] oneLongRow = new byte[1024 * 1024 + 1];
        Arrays.fill(oneLongRow, (byte) 'a');
        IllegalArgumentException e = assertThrows(IllegalArgumentException.class, () ->
            reader.read(new ByteArrayInputStream(oneLongRow))
        );
        assertTrue(e.getMessage().contains("1 MiB"));
    }

    @Test
    void testNewlinesResetRowLimit() throws Exception {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 3; i++) {
            sb.append("row".repeat(200_000)).append(i).append('\n');
        }
        List<MaskPair> pairs = reader.read(
            new ByteArrayInputStream(sb.toString().getBytes(StandardCharsets.UTF_8)));
        assertEquals(3, pairs.size());
    }

    @Test
    void testMaxPairsEnforced() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i <= 10_000; i++) {
            sb.append(i).append('\n');
        }
        IllegalArgumentException e = assertThrows(IllegalArgumentException.class, () ->
            reader.read(new ByteArrayInputStream(sb.toString().getBytes(StandardCharsets.UTF_8)))
        );
        assertTrue(e.getMessage().contains("10,000"));
    }

    @Test
    void testExactlyMaxPairsAllowed() throws Exception {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 10_000; i++) {
            sb.append(i).append('\n');
        }
        List<MaskPair> pairs = reader.read(
            new ByteArrayInputStream(sb.toString().getBytes(StandardCharsets.UTF_8)));
        assertEquals(10_000, pairs.size());
    }

    @Test
    void testBlankIdRejected() {
        LinePerPairReader blankIdReader = new LinePerPairReader() {
            @Override
            protected List<MaskPair> parse(String text) {
                return List.of(pair("  "));
            }
        };
        IllegalArgumentException e = assertThrows(IllegalArgumentException.class, () ->
            blankIdReader.read(new ByteArrayInputStream("x".getBytes(StandardCharsets.UTF_8)))
        );
        assertTrue(e.getMessage().contains("Missing ID"));
    }
}
