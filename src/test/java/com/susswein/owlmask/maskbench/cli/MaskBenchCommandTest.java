package com.susswein.owlmask.maskbench.cli;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import picocli.CommandLine;

import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class MaskBenchCommandTest {

    @Test
    void testMainCommandWithoutArgs() {
        MaskBenchCommand app = new MaskBenchCommand();
        CommandLine cmd = new CommandLine(app);

        int exitCode = cmd.execute();
        assertEquals(0, exitCode);
    }

    @Test
    void testJudgePairsCommand(@TempDir Path tempDir) {
        MaskBenchCommand app = new MaskBenchCommand();
        CommandLine cmd = new CommandLine(app);

        String reportDir = tempDir.resolve("reports").toString();
        
        int exitCode = cmd.execute("judge-pairs", "--pairs", "test-pairs.csv", "--format", "csv", "--report-dir", reportDir);
        assertEquals(0, exitCode);
    }

    @Test
    void testBenchmarkPairsCommand() {
        MaskBenchCommand app = new MaskBenchCommand();
        CommandLine cmd = new CommandLine(app);

        int exitCode = cmd.execute("benchmark-pairs", "--pairs", "test-pairs.jsonl", "--format", "jsonl");
        assertEquals(0, exitCode);
    }
}
