package com.susswein.owlmask.maskbench.llm;

import com.susswein.owlmask.maskbench.model.JudgeResult;

public interface JudgeProvider {
    JudgeResult evaluate(String prompt);
}
