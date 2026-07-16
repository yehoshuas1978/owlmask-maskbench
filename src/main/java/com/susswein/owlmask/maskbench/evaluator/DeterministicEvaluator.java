package com.susswein.owlmask.maskbench.evaluator;

import com.susswein.owlmask.maskbench.model.EntityLabel;
import com.susswein.owlmask.maskbench.model.MaskPair;

import java.util.HashMap;
import java.util.Map;

public class DeterministicEvaluator {

    public EvaluationResult evaluate(MaskPair maskPair) {
        String text = maskPair.text();
        String maskedText = maskPair.maskedText();
        
        // Compute full-value removal
        int removedCount = 0;
        int totalEntities = maskPair.entities().size();
        
        for (EntityLabel entity : maskPair.entities()) {
            String exactString = text.substring(entity.start(), entity.end());
            // An entity string should be completely missing from maskedText
            if (maskedText.contains(exactString)) {
                return new EvaluationResult(
                    false, 
                    "Entity '" + exactString + "' was not fully removed", 
                    buildMetrics(removedCount, totalEntities, maskPair.expectedPreserved().size(), 0)
                );
            }
            removedCount++;
        }
        
        // Check preservation
        int preservedCount = 0;
        int totalExpectedPreserved = maskPair.expectedPreserved().size();
        for (String expected : maskPair.expectedPreserved()) {
            if (!maskedText.contains(expected)) {
                return new EvaluationResult(
                    false, 
                    "Expected preserved value '" + expected + "' is missing", 
                    buildMetrics(removedCount, totalEntities, totalExpectedPreserved, preservedCount)
                );
            }
            preservedCount++;
        }
        
        return new EvaluationResult(
            true, 
            null, 
            buildMetrics(removedCount, totalEntities, totalExpectedPreserved, preservedCount)
        );
    }
    
    private Map<String, Object> buildMetrics(int removedCount, int totalEntities, int totalExpectedPreserved, int preservedCount) {
        Map<String, Object> metrics = new HashMap<>();
        metrics.put("entitiesRemoved", removedCount);
        metrics.put("totalEntities", totalEntities);
        metrics.put("valuesPreserved", preservedCount);
        metrics.put("totalExpectedPreserved", totalExpectedPreserved);
        return metrics;
    }
}
