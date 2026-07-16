package com.susswein.owlmask.maskbench.report;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.assertEquals;

class ReportGeneratorTest {

    @Test
    void testGenerateReports(@TempDir Path tempDir) throws IOException {
        ReportGenerator generator = new ReportGenerator(tempDir);
        generator.generateReports(5, 2, 1);

        // Verify CSV
        Path csvPath = tempDir.resolve("metrics.csv");
        assertTrue(Files.exists(csvPath), "CSV file should be created");
        String csvContent = Files.readString(csvPath);
        assertTrue(csvContent.contains("TotalPass,5"), "CSV should contain pass count");
        assertTrue(csvContent.contains("TotalFail,2"), "CSV should contain fail count");
        assertTrue(csvContent.contains("TotalIncomplete,1"), "CSV should contain incomplete count");

        // Verify JSON
        Path jsonPath = tempDir.resolve("report.json");
        assertTrue(Files.exists(jsonPath), "JSON file should be created");
        String jsonContent = Files.readString(jsonPath);
        assertTrue(jsonContent.contains("\"pass\": 5"), "JSON should contain pass count");
        assertTrue(jsonContent.contains("\"fail\": 2"), "JSON should contain fail count");
        assertTrue(jsonContent.contains("\"incomplete\": 1"), "JSON should contain incomplete count");

        // Verify JUnit XML
        Path xmlPath = tempDir.resolve("TEST-report.xml");
        assertTrue(Files.exists(xmlPath), "XML file should be created");
        String xmlContent = Files.readString(xmlPath);
        assertTrue(xmlContent.contains("tests=\"7\""), "XML should contain total tests");
        assertTrue(xmlContent.contains("failures=\"2\""), "XML should contain fail count");

        // Verify HTML
        Path htmlPath = tempDir.resolve("index.html");
        assertTrue(Files.exists(htmlPath), "HTML file should be created");
        String htmlContent = Files.readString(htmlPath);
        assertTrue(htmlContent.contains("Pass: 5"), "HTML should contain pass count");
        assertTrue(htmlContent.contains("Fail: 2"), "HTML should contain fail count");
    }
}
