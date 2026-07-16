package com.susswein.owlmask.maskbench.llm;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.tomakehurst.wiremock.WireMockServer;
import com.github.tomakehurst.wiremock.client.WireMock;
import com.github.tomakehurst.wiremock.core.WireMockConfiguration;
import com.susswein.owlmask.maskbench.model.JudgeConfig;
import com.susswein.owlmask.maskbench.model.JudgeResult;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.net.http.HttpClient;
import java.time.Duration;

import static com.github.tomakehurst.wiremock.client.WireMock.*;
import static org.junit.jupiter.api.Assertions.*;

class OpenAiCompatibleJudgeTest {

    private WireMockServer wireMockServer;
    private OpenAiCompatibleJudge judge;
    private ObjectMapper objectMapper = new ObjectMapper();

    @BeforeEach
    void setUp() {
        wireMockServer = new WireMockServer(WireMockConfiguration.wireMockConfig().dynamicPort());
        wireMockServer.start();
        WireMock.configureFor("localhost", wireMockServer.port());

        JudgeConfig config = new JudgeConfig(
                "test-judge",
                "openai",
                "http",
                "http://localhost:" + wireMockServer.port(),
                "gpt-4",
                "sk-test",
                0.0,
                100,
                1.0
        );

        // Fast retries for testing
        HttpClient httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(2))
                .build();
        judge = new OpenAiCompatibleJudge(config, httpClient, objectMapper, 3, 10, Duration.ofSeconds(30));
    }

    @AfterEach
    void tearDown() {
        if (wireMockServer != null) {
            wireMockServer.stop();
        }
    }

    @Test
    void testValidResponse() {
        stubFor(post(urlEqualTo("/v1/chat/completions"))
                .willReturn(aResponse()
                        .withStatus(200)
                        .withHeader("Content-Type", "application/json")
                        .withBody("""
                                {
                                  "choices": [
                                    {
                                      "message": {
                                        "content": "Hello world"
                                      }
                                    }
                                  ],
                                  "usage": {
                                    "prompt_tokens": 5,
                                    "completion_tokens": 2
                                  }
                                }
                                """)));

        JudgeResult result = judge.evaluate("Say hello");
        assertEquals("Hello world", result.content());
        assertEquals(5, result.promptTokens());
        assertEquals(2, result.completionTokens());
    }

    @Test
    void testMalformedResponse() {
        stubFor(post(urlEqualTo("/v1/chat/completions"))
                .willReturn(aResponse()
                        .withStatus(200)
                        .withHeader("Content-Type", "application/json")
                        .withBody("""
                                {
                                  "invalid": "json"
                                }
                                """)));

        RuntimeException exception = assertThrows(RuntimeException.class, () -> judge.evaluate("Test"));
        assertTrue(exception.getMessage().contains("Malformed response"));
    }

    @Test
    void testRateLimitRetriesAndSuccess() {
        // First 2 requests return 429, 3rd returns 200
        stubFor(post(urlEqualTo("/v1/chat/completions"))
                .inScenario("RateLimit")
                .whenScenarioStateIs(com.github.tomakehurst.wiremock.stubbing.Scenario.STARTED)
                .willReturn(aResponse().withStatus(429))
                .willSetStateTo("Retry1"));

        stubFor(post(urlEqualTo("/v1/chat/completions"))
                .inScenario("RateLimit")
                .whenScenarioStateIs("Retry1")
                .willReturn(aResponse().withStatus(429))
                .willSetStateTo("Success"));

        stubFor(post(urlEqualTo("/v1/chat/completions"))
                .inScenario("RateLimit")
                .whenScenarioStateIs("Success")
                .willReturn(aResponse()
                        .withStatus(200)
                        .withBody("""
                                {
                                  "choices": [{"message": {"content": "Success after rate limit"}}],
                                  "usage": {}
                                }
                                """)));

        JudgeResult result = judge.evaluate("Test");
        assertEquals("Success after rate limit", result.content());
        verify(3, postRequestedFor(urlEqualTo("/v1/chat/completions")));
    }

    @Test
    void testServerErrorRetriesAndFails() {
        // All requests return 500
        stubFor(post(urlEqualTo("/v1/chat/completions"))
                .willReturn(aResponse().withStatus(500)));

        RuntimeException exception = assertThrows(RuntimeException.class, () -> judge.evaluate("Test"));
        assertTrue(exception.getMessage().contains("Max retries exceeded"));
        verify(4, postRequestedFor(urlEqualTo("/v1/chat/completions"))); // 1 initial + 3 retries
    }

    @Test
    void testTimeoutRetries() {
        // WireMock delays the response to simulate timeout
        stubFor(post(urlEqualTo("/v1/chat/completions"))
                .inScenario("Timeout")
                .whenScenarioStateIs(com.github.tomakehurst.wiremock.stubbing.Scenario.STARTED)
                .willReturn(aResponse().withFixedDelay(2000).withStatus(200)) // 2 seconds delay
                .willSetStateTo("Success"));

        stubFor(post(urlEqualTo("/v1/chat/completions"))
                .inScenario("Timeout")
                .whenScenarioStateIs("Success")
                .willReturn(aResponse()
                        .withStatus(200)
                        .withBody("""
                                {
                                  "choices": [{"message": {"content": "Success after timeout"}}],
                                  "usage": {}
                                }
                                """)));

        JudgeConfig config = new JudgeConfig(
                "test", "openai", "http", "http://localhost:" + wireMockServer.port(),
                "gpt", "key", 0.0, 10, 1.0);
        HttpClient httpClient = HttpClient.newBuilder().build();
        OpenAiCompatibleJudge fastTimeoutJudge = new OpenAiCompatibleJudge(
                config, httpClient, objectMapper, 3, 10, Duration.ofMillis(500)); // 500ms timeout

        JudgeResult result = fastTimeoutJudge.evaluate("Test timeout");
        assertEquals("Success after timeout", result.content());
        verify(2, postRequestedFor(urlEqualTo("/v1/chat/completions")));
    }
}
