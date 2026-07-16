package com.susswein.owlmask.maskbench.report;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class ReportGenerator {

    private final Path reportDir;

    public ReportGenerator(Path reportDir) {
        this.reportDir = reportDir;
    }

    public void generateReports(int passCount, int failCount, int incompleteCount) throws IOException {
        Files.createDirectories(reportDir);
        
        // metrics.csv
        Path csvPath = reportDir.resolve("metrics.csv");
        String csvContent = "Metric,Value\n" +
                            "TotalPass," + passCount + "\n" +
                            "TotalFail," + failCount + "\n" +
                            "TotalIncomplete," + incompleteCount + "\n";
        Files.writeString(csvPath, csvContent);
        
        // report.json
        Path jsonPath = reportDir.resolve("report.json");
        String jsonContent = String.format("{\n  \"pass\": %d,\n  \"fail\": %d,\n  \"incomplete\": %d\n}", passCount, failCount, incompleteCount);
        Files.writeString(jsonPath, jsonContent);

        // JUnit XML stub
        Path junitPath = reportDir.resolve("TEST-report.xml");
        String junitContent = "<testsuite name=\"MaskBench\" tests=\"" + (passCount + failCount) + "\" failures=\"" + failCount + "\"></testsuite>";
        Files.writeString(junitPath, junitContent);
        
        // HTML stub
        Path htmlPath = reportDir.resolve("index.html");
        String htmlContent = "<html><body><h1>MaskBench Report</h1><p>Pass: " + passCount + "</p><p>Fail: " + failCount + "</p></body></html>";
        Files.writeString(htmlPath, htmlContent);
    }
}
