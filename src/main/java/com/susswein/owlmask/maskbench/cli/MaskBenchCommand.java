package com.susswein.owlmask.maskbench.cli;

import com.susswein.owlmask.maskbench.evaluator.DeterministicEvaluator;
import com.susswein.owlmask.maskbench.evaluator.EvaluationResult;
import com.susswein.owlmask.maskbench.io.CsvPairReader;
import com.susswein.owlmask.maskbench.io.JsonlPairReader;
import com.susswein.owlmask.maskbench.io.PairReader;
import com.susswein.owlmask.maskbench.model.MaskPair;
import com.susswein.owlmask.maskbench.report.ReportGenerator;
import picocli.CommandLine;
import picocli.CommandLine.Command;
import picocli.CommandLine.Option;

import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.Callable;

@Command(name = "owlmask-maskbench", mixinStandardHelpOptions = true, version = "1.0",
        description = "Java LLM Masking QA Harness",
        subcommands = {
            JudgePairsCommand.class,
            BenchmarkPairsCommand.class,
            ExplainCommand.class
        })
public class MaskBenchCommand implements Callable<Integer> {

    public static void main(String... args) {
        int exitCode = new CommandLine(new MaskBenchCommand()).execute(args);
        System.exit(exitCode);
    }

    @Override
    public Integer call() throws Exception {
        CommandLine.usage(this, System.out);
        return 0;
    }
}

@Command(name = "judge-pairs", description = "Judge masked pairs using deterministic rules and LLMs")
class JudgePairsCommand implements Callable<Integer> {

    @Option(names = {"--pairs"}, required = true, description = "Path to pairs file")
    String pairsPath;

    @Option(names = {"--format"}, required = true, description = "jsonl or csv")
    String format;

    @Option(names = {"--judges"}, description = "Path to judges cascade config")
    String judgesConfig;
    
    @Option(names = {"--assume-data-classification"}, description = "Override data classification for developer testing")
    String assumeDataClassification;

    @Option(names = {"--report-dir"}, description = "Output directory for reports", defaultValue = "build/pair-report")
    String reportDir;

    @Override
    public Integer call() {
        // Was: print a line, then write a hardcoded `generateReports(1, 0, 0)`
        // report — "we simulate a successful run". It never opened the pairs
        // file, so it reported **1 pass / 0 fail** for input that leaked every
        // identifier verbatim, and for a --pairs path that did not exist.
        //
        // This repo's own instructions say a bug here "does not crash anything;
        // it produces a confident wrong number", and that is precisely what a
        // fabricated pass is. Until the MultiJudgeCascade is actually wired,
        // refusing is the only honest behaviour: a visible gap beats a silent
        // false pass on a compliance-relevant measurement.
        System.err.println("""
                judge-pairs is not wired up.

                The LLM judge cascade (MultiJudgeCascade) exists and is unit
                tested, but this command never connected it to the pair reader
                or the report generator. It previously wrote a hardcoded
                "1 pass, 0 fail" report regardless of its input, so any report
                produced by an earlier build of this command is meaningless and
                should be discarded.

                Use instead:
                  * benchmark-pairs  -- the deterministic gate, fully wired
                  * owlmask-sdk's tools/scenario_validation/ + judge lanes,
                    which are what the language certification runs actually use
                """);
        return 2;
    }
}

@Command(name = "benchmark-pairs", description = "Benchmark masked pairs using only deterministic rules")
class BenchmarkPairsCommand implements Callable<Integer> {
    @Option(names = {"--pairs"}, required = true, description = "Path to pairs file")
    String pairsPath;

    @Option(names = {"--format"}, required = true, description = "jsonl or csv")
    String format;

    @Option(names = {"--report-dir"}, description = "Output directory for reports", defaultValue = "build/reports")
    String reportDir;

    /** All pairs passed. */
    static final int EXIT_OK = 0;
    /** The run completed and found failing pairs — usable as a CI gate. */
    static final int EXIT_FAILURES = 1;
    /** The run could not be performed at all (bad usage, unreadable input). */
    static final int EXIT_ERROR = 2;

    @Override
    public Integer call() {
        // Was: print one line and return 0 without ever opening --pairs.
        PairReader reader;
        switch (format == null ? "" : format.toLowerCase(Locale.ROOT)) {
            case "jsonl" -> reader = new JsonlPairReader();
            case "csv" -> reader = new CsvPairReader();
            default -> {
                System.err.println("Unsupported --format '" + format + "' (expected jsonl or csv)");
                return EXIT_ERROR;
            }
        }

        Path path = Paths.get(pairsPath);
        if (!Files.isReadable(path)) {
            System.err.println("Cannot read --pairs file: " + path.toAbsolutePath());
            return EXIT_ERROR;
        }

        List<MaskPair> pairs;
        try (InputStream in = Files.newInputStream(path)) {
            pairs = reader.read(in);
        } catch (Exception e) {
            System.err.println("Failed to read pairs: " + e.getMessage());
            return EXIT_ERROR;
        }

        // An empty file must not be reported as a clean pass — that is the
        // vacuous-green failure this command already shipped once.
        if (pairs.isEmpty()) {
            System.err.println("No pairs found in " + path + " — refusing to report a pass on an empty run.");
            return EXIT_ERROR;
        }

        DeterministicEvaluator evaluator = new DeterministicEvaluator();
        int passCount = 0;
        int failCount = 0;
        int withEntitySpans = 0;
        for (MaskPair pair : pairs) {
            if (!pair.entities().isEmpty()) {
                withEntitySpans++;
            }
            EvaluationResult result = evaluator.evaluate(pair);
            if (result.passed()) {
                passCount++;
            } else {
                failCount++;
                // The reason can quote a value that failed to be removed, so it
                // goes to stderr with the pair id and is never written into the
                // report files.
                System.err.println("FAIL " + pair.id() + ": " + result.reason());
            }
        }

        try {
            new ReportGenerator(Paths.get(reportDir)).generateReports(passCount, failCount, 0);
        } catch (Exception e) {
            System.err.println("Failed to write reports: " + e.getMessage());
            return EXIT_ERROR;
        }

        System.out.println("benchmark-pairs: " + pairs.size() + " pair(s), "
                + passCount + " passed, " + failCount + " failed");

        // Without `entities` spans the evaluator has no value to look for, so
        // it can only check `expectedPreserved` — it cannot detect a leak at
        // all. Saying so is the difference between "10 passed" meaning "nothing
        // leaked" and meaning "we did not look". Deliberately NOT solved by
        // adding a leak rule here: this repo already has two implementations
        // that disagree, and a third would make certification ambiguous.
        if (withEntitySpans == 0) {
            System.out.println("NOTE: no pair carried `entities` spans, so leak detection did not run. "
                    + "Only `expectedPreserved` was checked — a passing result here is NOT evidence "
                    + "that nothing leaked.");
        } else if (withEntitySpans < pairs.size()) {
            System.out.println("NOTE: only " + withEntitySpans + " of " + pairs.size()
                    + " pair(s) carried `entities` spans; leak detection ran on those only.");
        }

        System.out.println("Reports written to " + reportDir);
        return failCount == 0 ? EXIT_OK : EXIT_FAILURES;
    }
}

@Command(name = "explain", description = "Show explanations and examples for all maskbench commands")
class ExplainCommand implements Callable<Integer> {
    @Override
    public Integer call() throws Exception {
        System.out.println("OwlMask MaskBench Commands:");
        System.out.println("===========================\n");
        System.out.println("1. judge-pairs");
        System.out.println("   Explanation: Judges masked pairs using deterministic rules and LLMs.");
        System.out.println("                Evaluates how well masking was performed by running a cascade");
        System.out.println("                of LLM judges against provided data pairs.");
        System.out.println("   Example:     java -jar owlmask-maskbench.jar judge-pairs --pairs=data.csv --format=csv --report-dir=out\n");
        System.out.println("2. benchmark-pairs");
        System.out.println("   Explanation: Benchmarks masked pairs using only deterministic rules without LLMs.");
        System.out.println("                Useful for quick structural or exact-match validations.");
        System.out.println("   Example:     java -jar owlmask-maskbench.jar benchmark-pairs --pairs=data.jsonl --format=jsonl\n");
        System.out.println("3. explain");
        System.out.println("   Explanation: Shows this detailed explanation and examples for the commands.");
        System.out.println("   Example:     java -jar owlmask-maskbench.jar explain\n");
        return 0;
    }
}

