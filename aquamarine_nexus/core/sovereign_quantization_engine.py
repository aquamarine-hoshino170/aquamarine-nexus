import math
from typing import List, Tuple, Dict, Any

class SovereignQuantizationEngine:
    """
    High-Performance Zero-Dependency 8-bit & 4-bit Quantization Engine.
    Compresses continuous full-precision weights into compact byte representations.
    """

    @staticmethod
    def quantize_int8(weights: List[float]) -> Tuple[List[int], float]:
        """
        Symmetric INT8 Quantization:
        Scale S = max(|W|) / 127.0
        q = clamp(round(w / S), -128, 127)
        """
        max_val = max(abs(w) for w in weights) if weights else 1e-5
        scale = max_val / 127.0 if max_val > 0 else 1.0

        quantized = []
        inv_scale = 1.0 / scale
        for w in weights:
            q = int(round(w * inv_scale))
            q_clamped = max(-128, min(127, q))
            quantized.append(q_clamped)

        return quantized, scale

    @staticmethod
    def dequantize_int8(quantized: List[int], scale: float) -> List[float]:
        """Dequantizes INT8 back to floating point representation."""
        return [q * scale for q in quantized]

    @classmethod
    def quantize_int4_packed(cls, weights: List[float], block_size: int = 32) -> Dict[str, Any]:
        """
        Block-wise INT4 Quantization with Byte Packing:
        Packs two 4-bit nibbles (range 0..15) into a single 8-bit unsigned byte.
        Reduces memory footprint by 8x compared to FP32.
        """
        # Pad weights to match block size
        padded_weights = list(weights)
        remainder = len(padded_weights) % block_size
        if remainder != 0:
            padded_weights.extend([0.0] * (block_size - remainder))

        packed_bytes: List[int] = []
        scales: List[float] = []
        mins: List[float] = []

        for b_idx in range(0, len(padded_weights), block_size):
            block = padded_weights[b_idx : b_idx + block_size]
            min_val = min(block)
            max_val = max(block)
            diff = max_val - min_val
            scale = diff / 15.0 if diff > 0 else 1.0

            scales.append(scale)
            mins.append(min_val)

            # Quantize block into 0..15 integer domain
            inv_scale = 1.0 / scale
            q_nibbles = []
            for w in block:
                q = int(round((w - min_val) * inv_scale))
                q_clamped = max(0, min(15, q))
                q_nibbles.append(q_clamped)

            # Pack pairs of nibbles into bytes
            for i in range(0, len(q_nibbles), 2):
                low = q_nibbles[i]
                high = q_nibbles[i+1] if i + 1 < len(q_nibbles) else 0
                packed_byte = (high << 4) | low
                packed_bytes.append(packed_byte)

        return {
            "packed_data": packed_bytes,
            "scales": scales,
            "mins": mins,
            "original_length": len(weights),
            "block_size": block_size
        }

    @classmethod
    def dequantize_int4_packed(cls, payload: Dict[str, Any]) -> List[float]:
        """Unpacks 4-bit byte streams back into floating-point vectors."""
        packed_bytes = payload["packed_data"]
        scales = payload["scales"]
        mins = payload["mins"]
        orig_len = payload["original_length"]
        block_size = payload["block_size"]

        # Unpack nibbles
        unpacked_nibbles = []
        for byte_val in packed_bytes:
            low = byte_val & 0x0F
            high = (byte_val >> 4) & 0x0F
            unpacked_nibbles.extend([low, high])

        reconstructed: List[float] = []
        num_blocks = len(scales)

        for b_idx in range(num_blocks):
            scale = scales[b_idx]
            min_val = mins[b_idx]
            nibbles = unpacked_nibbles[b_idx * block_size : (b_idx + 1) * block_size]

            for q in nibbles:
                w = (q * scale) + min_val
                reconstructed.append(w)

        return reconstructed[:orig_len]
