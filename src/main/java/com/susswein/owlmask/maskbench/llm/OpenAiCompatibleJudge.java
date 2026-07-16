package com.susswein.owlmask.maskbench.llm;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.susswein.owlmask.maskbench.model.JudgeConfig;
import com.susswein.owlmask.maskbench.model.JudgeResult;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.Map;
import java.util.concurrent.ThreadLocalRandom;

public class OpenAiCompatibleJudge implements JudgeProvider {

    private final JudgeConfig config;
    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    private final int maxRetries;
    private final long baseDelayMs;
    private final Duration timeout;

    public OpenAiCompatibleJudge(JudgeConfig config) {
        this(config, HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(10)).build(), new ObjectMapper(), 5, 500, Duration.ofSeconds(30));
    }

    public OpenAiCompatibleJudge(JudgeConfig config, HttpClient httpClient, ObjectMapper objectMapper, int maxRetries, long baseDelayMs, Duration timeout) {
        this.config = config;
        this.httpClient = httpClient;
        this.objectMapper = objectMapper;
        this.maxRetries = maxRetries;
        this.baseDelayMs = baseDelayMs;
        this.timeout = timeout;
    }

    @Override
    public JudgeResult evaluate(String prompt) {
        int retries = 0;

        while (true) {
            try {
                String requestBody = createRequestBody(prompt);
                String url = config.baseUrl().endsWith("/v1/chat/completions") ? 
                        config.baseUrl() : 
                        config.baseUrl().replaceAll("/+$", "") + "/v1/chat/completions";

                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(url))
                        .header("Content-Type", "application/json")
                        .header("Authorization", "Bearer " + config.apiKey())
                        .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                        .timeout(timeout)
                        .build();

                HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

                if (response.statusCode() == 200) {
                    return parseResponse(response.body());
                } else if (response.statusCode() == 429 || response.statusCode() >= 500) {
                    if (retries >= maxRetries) {
                        throw new RuntimeException("Max retries exceeded. Last status: " + response.statusCode() + ", body: " + response.body());
                    }
                    sleepForBackoff(retries);
                    retries++;
                } else {
                    throw new RuntimeException("Unexpected status code: " + response.statusCode() + " body: " + response.body());
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Interrupted during request or backoff", e);
            } catch (RuntimeException e) {
                throw e;
            } catch (Exception e) {
                if (retries >= maxRetries) {
                    throw new RuntimeException("Request failed after retries", e);
                }
                sleepForBackoff(retries);
                retries++;
            }
        }
    }

    private void sleepForBackoff(int retryCount) {
        long delay = (long) (baseDelayMs * Math.pow(2, retryCount)) + ThreadLocalRandom.current().nextInt(10, 50);
        try {
            Thread.sleep(delay);
        } catch (InterruptedException ie) {
            Thread.currentThread().interrupt();
            throw new RuntimeException("Interrupted during backoff", ie);
        }
    }

    private String createRequestBody(String prompt) throws Exception {
        Map<String, Object> body = Map.of(
                "model", config.model(),
                "messages", new Object[]{
                        Map.of("role", "user", "content", prompt)
                },
                "temperature", config.temperature(),
                "max_tokens", config.maxOutputTokens()
        );
        return objectMapper.writeValueAsString(body);
    }

    private JudgeResult parseResponse(String responseBody) throws Exception {
        JsonNode root = objectMapper.readTree(responseBody);
        JsonNode messageNode = root.at("/choices/0/message/content");
        if (messageNode.isMissingNode() || !messageNode.isTextual()) {
            throw new RuntimeException("Malformed response: " + responseBody);
        }
        String content = messageNode.asText();
        
        int promptTokens = 0;
        int completionTokens = 0;
        JsonNode usageNode = root.get("usage");
        if (usageNode != null && !usageNode.isMissingNode()) {
            promptTokens = usageNode.path("prompt_tokens").asInt(0);
            completionTokens = usageNode.path("completion_tokens").asInt(0);
        }
        
        return new JudgeResult(content, promptTokens, completionTokens);
    }
}
