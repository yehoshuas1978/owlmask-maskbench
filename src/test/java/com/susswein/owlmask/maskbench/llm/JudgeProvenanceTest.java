package com.susswein.owlmask.maskbench.llm;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.susswein.owlmask.maskbench.model.JudgeConfig;
import com.susswein.owlmask.maskbench.model.JudgeResult;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.http.HttpClient;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * A judged verdict must say what produced it.
 *
 * An LLM verdict is not reproducible from its text alone. A judged certification
 * run is evidence about masking quality, and evidence that cannot be attributed
 * to a specific model, temperature and prompt is evidence that cannot be
 * defended or re-run — swapping the judge model would silently change the
 * numbers with nothing in the output to show it.
 */
class JudgeProvenanceTest {

    private HttpServer server;

    @AfterEach
    void tearDown() {
        if (server != null) {
            server.stop(0);
        }
    }

    private JudgeConfig startStubReturning(String content) throws IOException {
        server = HttpServer.create(new InetSocketAddress(0), 0);
        server.createContext("/v1/chat/completions", exchange -> {
            byte[] body = ("{\"choices\":[{\"message\":{\"content\":\"" + content + "\"}}],"
                    + "\"usage\":{\"prompt_tokens\":11,\"completion_tokens\":7}}")
                    .getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().add("Content-Type", "application/json");
            exchange.sendResponseHeaders(200, body.length);
            exchange.getResponseBody().write(body);
            exchange.close();
        });
        server.start();
        return new JudgeConfig("stub", "stub", "openai",
                "http://localhost:" + server.getAddress().getPort(),
                "gpt-test-4", "key", 0.25, 256, 1.0);
    }

    private OpenAiCompatibleJudge judgeFor(JudgeConfig config) {
        return new OpenAiCompatibleJudge(config, HttpClient.newHttpClient(),
                new ObjectMapper(), 0, 1, Duration.ofSeconds(5));
    }

    @Test
    void aVerdictCarriesTheModelTemperatureAndPromptVersion() throws Exception {
        JudgeConfig config = startStubReturning("NO_ADDITIONAL_FINDING");

        JudgeResult result = judgeFor(config).evaluate("prompt");

        assertEquals("gpt-test-4", result.model());
        assertEquals(0.25, result.temperature());
        assertNotNull(result.promptVersion());
        assertEquals(OpenAiCompatibleJudge.PROMPT_VERSION, result.promptVersion());
    }

    @Test
    void theContentAndTokenCountsStillComeThrough() throws Exception {
        // The provenance fields are additive; the existing contract must not move.
        JudgeConfig config = startStubReturning("NO_ADDITIONAL_FINDING");

        JudgeResult result = judgeFor(config).evaluate("prompt");

        assertEquals("NO_ADDITIONAL_FINDING", result.content());
        assertEquals(11, result.promptTokens());
        assertEquals(7, result.completionTokens());
    }

    @Test
    void aVerdictWithProvenanceIsAttributable() throws Exception {
        JudgeConfig config = startStubReturning("NO_ADDITIONAL_FINDING");

        assertTrue(judgeFor(config).evaluate("prompt").isAttributable());
    }

    @Test
    void aVerdictBuiltWithoutProvenanceIsNotAttributable() {
        // The legacy three-arg constructor still compiles for callers written
        // before this, but it must not claim to be attributable.
        JudgeResult legacy = new JudgeResult("NO_ADDITIONAL_FINDING", 1, 1);

        assertFalse(legacy.isAttributable());
        assertEquals(null, legacy.model());
    }

    @Test
    void twoDifferentModelsProduceDistinguishableVerdicts() throws Exception {
        // The point of the whole change: identical verdict text from different
        // judges must not be indistinguishable in the record.
        JudgeConfig first = startStubReturning("NO_ADDITIONAL_FINDING");
        JudgeResult a = judgeFor(first).evaluate("prompt");

        JudgeConfig second = new JudgeConfig("stub", "stub", "openai", first.baseUrl(),
                "claude-test-5", "key", 0.9, 256, 1.0);
        JudgeResult b = judgeFor(second).evaluate("prompt");

        assertEquals(a.content(), b.content());
        assertFalse(a.model().equals(b.model()) && a.temperature().equals(b.temperature()));
    }
}
