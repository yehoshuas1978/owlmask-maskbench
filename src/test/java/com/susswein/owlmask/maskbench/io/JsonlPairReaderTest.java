package com.susswein.owlmask.maskbench.io;

import com.susswein.owlmask.maskbench.model.MaskPair;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class JsonlPairReaderTest {
    private final JsonlPairReader reader = new JsonlPairReader();

    @Test
    void testValidJsonl() throws Exception {
        String jsonl = "{\"id\":\"1\",\"text\":\"hello\",\"maskedText\":\"***\"}\n" +
                       "{\"id\":\"2\",\"text\":\"world\",\"maskedText\":\"***\"}";
        List<MaskPair> pairs = reader.read(new ByteArrayInputStream(jsonl.getBytes(StandardCharsets.UTF_8)));
        assertEquals(2, pairs.size());
        assertEquals("1", pairs.get(0).id());
        assertEquals("hello", pairs.get(0).text());
        assertEquals("2", pairs.get(1).id());
    }

    @Test
    void testMissingRequiredColumns() {
        String jsonl = "{\"id\":\"1\",\"text\":\"hello\"}";
        assertThrows(IllegalArgumentException.class, () -> 
            reader.read(new ByteArrayInputStream(jsonl.getBytes(StandardCharsets.UTF_8)))
        );
    }

    @Test
    void testDuplicateIds() {
        String jsonl = "{\"id\":\"1\",\"text\":\"hello\",\"maskedText\":\"***\"}\n" +
                       "{\"id\":\"1\",\"text\":\"world\",\"maskedText\":\"***\"}";
        assertThrows(IllegalArgumentException.class, () -> 
            reader.read(new ByteArrayInputStream(jsonl.getBytes(StandardCharsets.UTF_8)))
        );
    }

    @Test
    void testUtf8Bom() throws Exception {
        byte[] bom = new byte[] { (byte)0xEF, (byte)0xBB, (byte)0xBF };
        byte[] content = "{\"id\":\"1\",\"text\":\"hello\",\"maskedText\":\"***\"}".getBytes(StandardCharsets.UTF_8);
        byte[] all = new byte[bom.length + content.length];
        System.arraycopy(bom, 0, all, 0, bom.length);
        System.arraycopy(content, 0, all, bom.length, content.length);
        
        List<MaskPair> pairs = reader.read(new ByteArrayInputStream(all));
        assertEquals(1, pairs.size());
    }

    @Test
    void testInvalidUtf8() {
        byte[] invalid = new byte[] { (byte)0xC3, 0x28 }; // Invalid UTF-8 sequence
        assertThrows(IllegalArgumentException.class, () -> 
            reader.read(new ByteArrayInputStream(invalid))
        );
    }
}
