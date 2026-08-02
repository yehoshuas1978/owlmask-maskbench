package com.susswein.owlmask.maskbench.cli;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import picocli.CommandLine;

import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * These tests previously asserted only {@code exitCode == 0} while pointing at
 * {@code test-pairs.csv}, a file that does not exist. Both commands were stubs
 * that returned 0 without reading anything, so the assertions could not fail —
 * they guarded nothing while reporting green.
 *
 * Every test here now distinguishes a real pass from a fabricated one.
 */
class MaskBenchCommandTest {

    private static final String CLEAN_PAIR = """
            {"id":"ok-1","locale":"en-US","domain":"insurance","dataClassification":"synthetic",\
            "text":"Claim for John Smith.","maskedText":"Claim for [PERSON].",\
            "expectedPreserved":["Claim for"]}
            """;

    /** {@code expectedPreserved} names a phrase the masking destroyed. */
    private static final String FAILING_PAIR = """
            {"id":"bad-1","locale":"en-US","domain":"insurance","dataClassification":"synthetic",\
            "text":"Diagnosis: Type 2 Diabetes for John Smith.","maskedText":"[REDACTED]",\
            "expectedPreserved":["Type 2 Diabetes"]}
            """;

    private static int run(String... args) {
        return new CommandLine(new MaskBenchCommand()).execute(args);
    }

    @Test
    void bareCommandPrintsUsage() {
        assertEquals(0, run());
    }

    @Test
    void benchmarkPairsPassesOnCleanInput(@TempDir Path tempDir) throws Exception {
        Path pairs = Files.writeString(tempDir.resolve("pairs.jsonl"), CLEAN_PAIR);
        Path reports = tempDir.resolve("reports");

        assertEquals(0, run("benchmark-pairs", "--pairs", pairs.toString(),
                "--format", "jsonl", "--report-dir", reports.toString()));

        String report = Files.readString(reports.resolve("report.json"));
        assertTrue(report.contains("\"pass\": 1"), report);
        assertTrue(report.contains("\"fail\": 0"), report);
    }

    @Test
    void benchmarkPairsFailsOnAFailingPair(@TempDir Path tempDir) throws Exception {
        Path pairs = Files.writeString(tempDir.resolve("pairs.jsonl"), FAILING_PAIR);
        Path reports = tempDir.resolve("reports");

        // Exit 1, not 0 — this is what makes the command usable as a gate, and
        // what the stub could never do.
        assertEquals(1, run("benchmark-pairs", "--pairs", pairs.toString(),
                "--format", "jsonl", "--report-dir", reports.toString()));

        String report = Files.readString(reports.resolve("report.json"));
        assertTrue(report.contains("\"fail\": 1"), report);
        assertTrue(report.contains("\"pass\": 0"), report);
    }

    @Test
    void benchmarkPairsCountsAMixedRun(@TempDir Path tempDir) throws Exception {
        Path pairs = Files.writeString(tempDir.resolve("pairs.jsonl"), CLEAN_PAIR + FAILING_PAIR);
        Path reports = tempDir.resolve("reports");

        assertEquals(1, run("benchmark-pairs", "--pairs", pairs.toString(),
                "--format", "jsonl", "--report-dir", reports.toString()));

        String report = Files.readString(reports.resolve("report.json"));
        assertTrue(report.contains("\"pass\": 1"), report);
        assertTrue(report.contains("\"fail\": 1"), report);
    }

    @Test
    void benchmarkPairsRefusesAMissingFile(@TempDir Path tempDir) {
        Path reports = tempDir.resolve("reports");

        assertEquals(2, run("benchmark-pairs", "--pairs",
                tempDir.resolve("absent.jsonl").toString(),
                "--format", "jsonl", "--report-dir", reports.toString()));

        // The decisive part: no report is produced. The stub wrote a passing
        // report for a nonexistent input.
        assertFalse(Files.exists(reports.resolve("report.json")),
                "a report must not exist for a run that never happened");
    }

    @Test
    void benchmarkPairsRefusesAnEmptyFile(@TempDir Path tempDir) throws Exception {
        Path pairs = Files.writeString(tempDir.resolve("empty.jsonl"), "");
        Path reports = tempDir.resolve("reports");

        assertEquals(2, run("benchmark-pairs", "--pairs", pairs.toString(),
                "--format", "jsonl", "--report-dir", reports.toString()));
        assertFalse(Files.exists(reports.resolve("report.json")),
                "an empty run must not be reported as a clean pass");
    }

    @Test
    void benchmarkPairsRejectsAnUnknownFormat(@TempDir Path tempDir) throws Exception {
        Path pairs = Files.writeString(tempDir.resolve("pairs.jsonl"), CLEAN_PAIR);

        assertEquals(2, run("benchmark-pairs", "--pairs", pairs.toString(),
                "--format", "yaml", "--report-dir", tempDir.resolve("r").toString()));
    }

    @Test
    void judgePairsRefusesRatherThanFabricatingAPass(@TempDir Path tempDir) throws Exception {
        Path pairs = Files.writeString(tempDir.resolve("pairs.jsonl"), FAILING_PAIR);
        Path reports = tempDir.resolve("reports");

        assertEquals(2, run("judge-pairs", "--pairs", pairs.toString(),
                "--format", "jsonl", "--report-dir", reports.toString()));

        // It used to write {"pass":1,"fail":0} here no matter what.
        assertFalse(Files.exists(reports.resolve("report.json")),
                "judge-pairs must not write a report while it is unwired");
    }
}
