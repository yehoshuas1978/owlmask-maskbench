package com.susswein.owlmask.maskbench.evaluator;

import com.susswein.owlmask.maskbench.model.DataClassification;
import com.susswein.owlmask.maskbench.model.EntityLabel;
import com.susswein.owlmask.maskbench.model.MaskPair;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class DeterministicEvaluatorTest {

    private final DeterministicEvaluator evaluator = new DeterministicEvaluator();

    @Test
    void testSuccessfulEvaluation() {
        String originalText = "Hello John Doe, your email is john@example.com";
        String maskedText = "Hello [NAME], your email is [EMAIL]";
        
        EntityLabel nameEntity = new EntityLabel(6, 14, "NAME", "HIGH");
        EntityLabel emailEntity = new EntityLabel(30, 46, "EMAIL", "HIGH");
        
        MaskPair pair = new MaskPair(
                "id1", "en", "test", DataClassification.SYNTHETIC, originalText, maskedText,
                List.of(nameEntity, emailEntity),
                List.of("Hello", "your email is")
        );
        
        EvaluationResult result = evaluator.evaluate(pair);
        assertTrue(result.passed());
        assertNull(result.reason());
        assertEquals(2, result.metrics().get("entitiesRemoved"));
        assertEquals(2, result.metrics().get("valuesPreserved"));
    }

    @Test
    void testEntityNotRemoved() {
        String originalText = "Hello John Doe";
        String maskedText = "Hello John Doe"; 
        
        EntityLabel nameEntity = new EntityLabel(6, 14, "NAME", "HIGH");
        
        MaskPair pair = new MaskPair(
                "id2", "en", "test", DataClassification.SYNTHETIC, originalText, maskedText,
                List.of(nameEntity),
                List.of("Hello")
        );
        
        EvaluationResult result = evaluator.evaluate(pair);
        assertFalse(result.passed());
        assertNotNull(result.reason());
        assertTrue(result.reason().contains("John Doe"));
        assertEquals(0, result.metrics().get("entitiesRemoved"));
    }

    @Test
    void testPreservedValueMissing() {
        String originalText = "Hello John Doe";
        String maskedText = "Hi [NAME]";
        
        EntityLabel nameEntity = new EntityLabel(6, 14, "NAME", "HIGH");
        
        MaskPair pair = new MaskPair(
                "id3", "en", "test", DataClassification.SYNTHETIC, originalText, maskedText,
                List.of(nameEntity),
                List.of("Hello") 
        );
        
        EvaluationResult result = evaluator.evaluate(pair);
        assertFalse(result.passed());
        assertNotNull(result.reason());
        assertTrue(result.reason().contains("Hello"));
        assertEquals(1, result.metrics().get("entitiesRemoved"));
        assertEquals(0, result.metrics().get("valuesPreserved"));
    }
}
