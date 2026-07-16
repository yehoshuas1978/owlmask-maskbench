package com.susswein.owlmask.maskbench.cascade;

import com.susswein.owlmask.maskbench.evaluator.DeterministicEvaluator;
import com.susswein.owlmask.maskbench.evaluator.EvaluationResult;
import com.susswein.owlmask.maskbench.llm.JudgeProvider;
import com.susswein.owlmask.maskbench.model.JudgeResult;
import com.susswein.owlmask.maskbench.model.MaskPair;

import java.util.List;

public class MultiJudgeCascade {

    private final DeterministicEvaluator deterministicEvaluator;
    private final List<JudgeProvider> judgeProviders;

    public MultiJudgeCascade(DeterministicEvaluator deterministicEvaluator, List<JudgeProvider> judgeProviders) {
        this.deterministicEvaluator = deterministicEvaluator;
        this.judgeProviders = judgeProviders;
    }

    public CascadeResult evaluate(MaskPair pair) {
        try {
            EvaluationResult detResult = deterministicEvaluator.evaluate(pair);
            if (!detResult.passed()) {
                return CascadeResult.FAIL;
            }
        } catch (Exception e) {
            return CascadeResult.FAIL;
        }

        String prompt = buildPrompt(pair);

        for (JudgeProvider judge : judgeProviders) {
            try {
                JudgeResult result = judge.evaluate(prompt);
                String content = result.content();
                
                // If judge finding is NOT exactly NO_ADDITIONAL_FINDING, it's a fail.
                if (content == null || !content.contains("NO_ADDITIONAL_FINDING")) {
                    return CascadeResult.FAIL;
                }
            } catch (Exception e) {
                // Return FAIL on timeout, rate limit, provider error (fail-closed cascade)
                return CascadeResult.FAIL;
            }
        }

        return CascadeResult.PASS;
    }
    
    private String buildPrompt(MaskPair pair) {
        return "Please review the following masking output for residual PII:\n" +
               "Original: " + pair.text() + "\n" +
               "Masked: " + pair.maskedText() + "\n" +
               "Reply strictly with 'NO_ADDITIONAL_FINDING' or a JSON array of findings.";
    }
}
