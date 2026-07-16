package com.susswein.owlmask.maskbench.io;

import com.susswein.owlmask.maskbench.model.MaskPair;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.charset.CharacterCodingException;
import java.nio.charset.CharsetDecoder;
import java.nio.charset.CodingErrorAction;
import java.nio.charset.StandardCharsets;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public abstract class BasePairReader implements PairReader {
    protected static final int MAX_TOTAL_BYTES = 10 * 1024 * 1024; // 10 MiB
    protected static final int MAX_ROW_BYTES = 1024 * 1024; // 1 MiB
    protected static final int MAX_PAIRS = 10000;

    @Override
    public List<MaskPair> read(InputStream inputStream) throws Exception {
        byte[] data = readAllBytes(inputStream, MAX_TOTAL_BYTES);
        String text = decodeUtf8(data);
        if (text.startsWith("\uFEFF")) {
            text = text.substring(1);
        }
        
        List<MaskPair> pairs = parse(text);
        
        if (pairs.size() > MAX_PAIRS) {
            throw new IllegalArgumentException("Max 10,000 pairs allowed");
        }
        
        Set<String> ids = new HashSet<>();
        for (MaskPair pair : pairs) {
            if (pair.id() == null || pair.id().trim().isEmpty()) {
                throw new IllegalArgumentException("Missing ID");
            }
            if (!ids.add(pair.id())) {
                throw new IllegalArgumentException("Duplicate ID: " + pair.id());
            }
        }
        
        return pairs;
    }

    protected abstract List<MaskPair> parse(String text) throws Exception;

    private byte[] readAllBytes(InputStream in, int maxBytes) throws Exception {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        byte[] buffer = new byte[8192];
        int read;
        int total = 0;
        int currentRowBytes = 0;
        while ((read = in.read(buffer)) != -1) {
            total += read;
            if (total > maxBytes) {
                throw new IllegalArgumentException("Total input exceeds max of 10 MiB");
            }
            for (int i = 0; i < read; i++) {
                if (buffer[i] == '\n') {
                    currentRowBytes = 0;
                } else {
                    currentRowBytes++;
                    if (currentRowBytes > MAX_ROW_BYTES) {
                        throw new IllegalArgumentException("Row exceeds max of 1 MiB");
                    }
                }
            }
            baos.write(buffer, 0, read);
        }
        return baos.toByteArray();
    }

    private String decodeUtf8(byte[] data) throws Exception {
        CharsetDecoder decoder = StandardCharsets.UTF_8.newDecoder()
                .onMalformedInput(CodingErrorAction.REPORT)
                .onUnmappableCharacter(CodingErrorAction.REPORT);
        try {
            return decoder.decode(ByteBuffer.wrap(data)).toString();
        } catch (CharacterCodingException e) {
            throw new IllegalArgumentException("Invalid UTF-8 encoding", e);
        }
    }
}
