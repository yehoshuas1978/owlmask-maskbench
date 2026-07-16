package com.susswein.owlmask.maskbench.io;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.susswein.owlmask.maskbench.model.DataClassification;
import com.susswein.owlmask.maskbench.model.EntityLabel;
import com.susswein.owlmask.maskbench.model.MaskPair;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;

import java.io.StringReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class CsvPairReader extends BasePairReader {
    private final ObjectMapper mapper = new ObjectMapper();

    @Override
    protected List<MaskPair> parse(String text) throws Exception {
        List<MaskPair> pairs = new ArrayList<>();
        CSVFormat format = CSVFormat.DEFAULT.builder()
                .setHeader()
                .setSkipHeaderRecord(true)
                .build();
                
        try (CSVParser parser = format.parse(new StringReader(text))) {
            for (CSVRecord record : parser) {
                if (!record.isMapped("id") || !record.isMapped("text") || !record.isMapped("maskedText")) {
                    throw new IllegalArgumentException("Missing required columns");
                }
                
                long rowLength = 0;
                for (String value : record) {
                    rowLength += value.getBytes(StandardCharsets.UTF_8).length;
                }
                if (rowLength > MAX_ROW_BYTES) {
                    throw new IllegalArgumentException("Row exceeds max of 1 MiB");
                }
                
                String id = record.get("id");
                String locale = record.isMapped("locale") ? record.get("locale") : null;
                String domain = record.isMapped("domain") ? record.get("domain") : null;
                String dataClassificationStr = record.isMapped("dataClassification") ? record.get("dataClassification") : null;
                DataClassification dataClassification = null;
                if (dataClassificationStr != null && !dataClassificationStr.trim().isEmpty()) {
                    dataClassification = DataClassification.fromValue(dataClassificationStr);
                }
                
                String textVal = record.get("text");
                String maskedTextVal = record.get("maskedText");
                
                List<EntityLabel> entities = new ArrayList<>();
                if (record.isMapped("entities")) {
                    String entitiesStr = record.get("entities");
                    if (entitiesStr != null && !entitiesStr.trim().isEmpty()) {
                        entities = mapper.readValue(entitiesStr, new TypeReference<List<EntityLabel>>() {});
                    }
                }
                
                List<String> expectedPreserved = new ArrayList<>();
                if (record.isMapped("expectedPreserved")) {
                    String epStr = record.get("expectedPreserved");
                    if (epStr != null && !epStr.trim().isEmpty()) {
                        expectedPreserved = mapper.readValue(epStr, new TypeReference<List<String>>() {});
                    }
                }
                
                pairs.add(new MaskPair(id, locale, domain, dataClassification, textVal, maskedTextVal, entities, expectedPreserved));
            }
        } catch (IllegalArgumentException e) {
            throw e;
        } catch (Exception e) {
            throw new IllegalArgumentException("Invalid CSV: " + e.getMessage(), e);
        }
        return pairs;
    }
}
