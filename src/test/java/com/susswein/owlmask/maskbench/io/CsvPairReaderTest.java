package com.susswein.owlmask.maskbench.io;

import com.susswein.owlmask.maskbench.model.MaskPair;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class CsvPairReaderTest {
    private final CsvPairReader reader = new CsvPairReader();

    @Test
    void testValidCsv() throws Exception {
        String csv = "id,text,maskedText\n" +
                     "1,hello,***\n" +
                     "2,world,***";
        List<MaskPair> pairs = reader.read(new ByteArrayInputStream(csv.getBytes(StandardCharsets.UTF_8)));
        assertEquals(2, pairs.size());
        assertEquals("1", pairs.get(0).id());
        assertEquals("hello", pairs.get(0).text());
        assertEquals("2", pairs.get(1).id());
    }

    @Test
    void testMissingRequiredColumns() {
        String csv = "id,text\n1,hello";
        assertThrows(IllegalArgumentException.class, () -> 
            reader.read(new ByteArrayInputStream(csv.getBytes(StandardCharsets.UTF_8)))
        );
    }

    @Test
    void testDuplicateIds() {
        String csv = "id,text,maskedText\n" +
                     "1,hello,***\n" +
                     "1,world,***";
        assertThrows(IllegalArgumentException.class, () -> 
            reader.read(new ByteArrayInputStream(csv.getBytes(StandardCharsets.UTF_8)))
        );
    }

    @Test
    void testUtf8Bom() throws Exception {
        byte[] bom = new byte[] { (byte)0xEF, (byte)0xBB, (byte)0xBF };
        byte[] content = ("id,text,maskedText\n" +
                         "1,hello,***").getBytes(StandardCharsets.UTF_8);
        byte[] all = new byte[bom.length + content.length];
        System.arraycopy(bom, 0, all, 0, bom.length);
        System.arraycopy(content, 0, all, bom.length, content.length);
        
        List<MaskPair> pairs = reader.read(new ByteArrayInputStream(all));
        assertEquals(1, pairs.size());
    }
}
