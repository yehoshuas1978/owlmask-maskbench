package com.susswein.owlmask.maskbench.cascade;

import com.susswein.owlmask.maskbench.evaluator.DeterministicEvaluator;
import com.susswein.owlmask.maskbench.evaluator.EvaluationResult;
import com.susswein.owlmask.maskbench.llm.JudgeProvider;
import com.susswein.owlmask.maskbench.model.DataClassification;
import com.susswein.owlmask.maskbench.model.JudgeResult;
import com.susswein.owlmask.maskbench.model.MaskPair;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;

class MultiJudgeCascadeTest {

    private MaskPair pair;

    @BeforeEach
    void setUp() {
        pair = new MaskPair("id", "en", "finance", DataClassification.SYNTHETIC, "text", "maskedText", List.of(), List.of());
    }

    @Test
    void testDeterministicFailReturnsFailImmediately() {
        DeterministicEvaluator detEval = new DeterministicEvaluator() {
            @Override
            public EvaluationResult evaluate(MaskPair pair) {
                return new EvaluationResult(false, "reason", Map.of());
            }
        };
        JudgeProvider judge = prompt -> { throw new RuntimeException("Should not be called"); };
        
        MultiJudgeCascade cascade = new MultiJudgeCascade(detEval, List.of(judge));
        assertEquals(CascadeResult.FAIL, cascade.evaluate(pair));
    }

    @Test
    void testJudgeFindingReturnsFail() {
        DeterministicEvaluator detEval = new DeterministicEvaluator() {
            @Override
            public EvaluationResult evaluate(MaskPair pair) {
                return new EvaluationResult(true, null, Map.of());
            }
        };
        JudgeProvider judge1 = prompt -> new JudgeResult("{ \"finding\": \"PII found\" }", 10, 10);
        JudgeProvider judge2 = prompt -> { throw new RuntimeException("Should not be called"); };
        
        MultiJudgeCascade cascade = new MultiJudgeCascade(detEval, List.of(judge1, judge2));
        assertEquals(CascadeResult.FAIL, cascade.evaluate(pair));
    }

    @Test
    void testJudgeExceptionReturnsFailByDefault() {
        DeterministicEvaluator detEval = new DeterministicEvaluator() {
            @Override
            public EvaluationResult evaluate(MaskPair pair) {
                return new EvaluationResult(true, null, Map.of());
            }
        };
        JudgeProvider judge1 = prompt -> new JudgeResult("NO_ADDITIONAL_FINDING", 10, 10);
        JudgeProvider judge2 = prompt -> { throw new RuntimeException("Network error"); };
        
        MultiJudgeCascade cascade = new MultiJudgeCascade(detEval, List.of(judge1, judge2));
        assertEquals(CascadeResult.FAIL, cascade.evaluate(pair));
    }

    @Test
    void testAllPassReturnsPass() {
        DeterministicEvaluator detEval = new DeterministicEvaluator() {
            @Override
            public EvaluationResult evaluate(MaskPair pair) {
                return new EvaluationResult(true, null, Map.of());
            }
        };
        JudgeProvider judge1 = prompt -> new JudgeResult("NO_ADDITIONAL_FINDING", 10, 10);
        JudgeProvider judge2 = prompt -> new JudgeResult("NO_ADDITIONAL_FINDING", 10, 10);
        
        MultiJudgeCascade cascade = new MultiJudgeCascade(detEval, List.of(judge1, judge2));
        assertEquals(CascadeResult.PASS, cascade.evaluate(pair));
    }
}
