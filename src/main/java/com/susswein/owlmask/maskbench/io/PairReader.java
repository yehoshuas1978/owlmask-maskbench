package com.susswein.owlmask.maskbench.io;

import com.susswein.owlmask.maskbench.model.MaskPair;
import java.io.InputStream;
import java.util.List;

public interface PairReader {
    List<MaskPair> read(InputStream inputStream) throws Exception;
}
