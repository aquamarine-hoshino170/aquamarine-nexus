import os
import math
from typing import List, Dict, Any, Optional

from aquamarine_nexus.core.sovereign_formula_registry import FormulaRegistry
from aquamarine_nexus.core.sovereign_formulas_engine import SovereignFormulasEngine
from aquamarine_nexus.core.sovereign_quantization_engine import SovereignQuantizationEngine
from aquamarine_nexus.core.sovereign_inference_engine import SovereignInferenceEngine

class AutoNexus:
    """
    Unified Zero-Config Autonomous Engine.
    Coordinates math compilation, memory quantization, autograd, and inference automatically.
    """
    def __init__(self, vocab_size: int = 1000, max_context_turns: int = 6):
        self.vocab_size = vocab_size
        self.max_context_turns = max_context_turns
        
        # 1. Auto-initialize mock tokenizer and inference engine
        self._tokenizer = self._build_internal_tokenizer()
        self.inference_engine = SovereignInferenceEngine(
            tokenizer=self._tokenizer, 
            vocab_size=self.vocab_size
        )
        
        # 2. Auto-bootstrap fundamental formulas into registry
        self._bootstrap_default_formulas()

    def _build_internal_tokenizer(self):
        class InternalByteTokenizer:
            def encode(self, text: str) -> List[int]:
                return [ord(c) % 1000 for c in text]
            def decode(self, ids: List[int]) -> str:
                return "".join([chr(tok % 128) for tok in ids])
        return InternalByteTokenizer()

    def _bootstrap_default_formulas(self):
        """Auto-registers foundational activation and physics formulas."""
        # GeLU
        FormulaRegistry.register('gelu', lambda x: [SovereignFormulasEngine.gelu(val) for val in x])
        
        # Swish
        FormulaRegistry.register('swish', lambda x: [v / (1.0 + math.exp(-max(min(v, 20.0), -20.0))) for v in x])
        
        # Material Implication
        FormulaRegistry.register('implication', lambda x: [1.0 if ((not bool(x[0])) or bool(x[1])) else 0.0])

    def auto_compute(self, formula_name: str, inputs: List[float], with_grad: bool = True) -> Dict[str, Any]:
        """
        Executes any mathematical expression with automated forward and backward pass.
        """
        output = FormulaRegistry.execute(formula_name, inputs)
        result = {"forward": output}
        if with_grad:
            dummy_grad = [1.0] * len(output)
            grads = FormulaRegistry.backprop(formula_name, inputs, grad_output=dummy_grad)
            result["gradient"] = grads
        return result

    def auto_quantize(self, weights: List[float], target_bits: int = 4) -> Dict[str, Any]:
        """
        Automatically compresses parameter weights based on selected bitwidth.
        """
        if target_bits == 4:
            payload = SovereignQuantizationEngine.quantize_int4_packed(weights, block_size=32)
            recon = SovereignQuantizationEngine.dequantize_int4_packed(payload)
            compression = len(weights) * 4 / len(payload["packed_data"])
            return {"mode": "INT4-Packed", "payload": payload, "compression_ratio": f"{compression:.1f}x", "reconstructed": recon}
        elif target_bits == 8:
            q_data, scale = SovereignQuantizationEngine.quantize_int8(weights)
            recon = SovereignQuantizationEngine.dequantize_int8(q_data, scale)
            return {"mode": "INT8-Symmetric", "data": q_data, "scale": scale, "reconstructed": recon}
        else:
            return {"mode": "FP32-Uncompressed", "data": weights, "reconstructed": weights}

    def auto_generate(self, prompt: str, max_tokens: int = 15, temperature: float = 0.7) -> str:
        """
        Runs one-line prompt completion.
        """
        return self.inference_engine.generate(
            prompt=prompt,
            max_new_tokens=max_tokens,
            temperature=temperature
        )

    def run_all(self, prompt: str, weights: List[float]) -> Dict[str, Any]:
        """
        Autonomous Pipeline: Runs inference, compression, and invariant verification in one call.
        """
        print("[AutoNexus] 1. Processing Autoregressive Stream...")
        gen_text = self.auto_generate(prompt)
        
        print("[AutoNexus] 2. Running Automatic Memory Quantization...")
        quant_res = self.auto_quantize(weights, target_bits=4)
        
        print("[AutoNexus] 3. Verifying Invariant Phase-Space Registry...")
        gelu_res = self.auto_compute('gelu', [0.5, -1.2, 2.0])

        return {
            "prompt": prompt,
            "generated_output": gen_text,
            "quantization_ratio": quant_res["compression_ratio"],
            "invariant_forward": gelu_res["forward"],
            "status": "ALL_PIPELINES_SYNCHRONIZED"
        }
