import math
import array
from typing import List, Tuple, Dict, Any

class QuantizedTensorCore:
    """
    Zero-Dependency High-Density Tensor Quantization Engine.
    Compresses Float64/Float32 tensors into INT8 (8-bit signed) representations
    with dynamic scaling factors and zero-point alignment, reducing memory footprint by 4x-8x.
    """

    @staticmethod
    def quantize_f64_to_int8(data: List[float]) -> Tuple[array.array, float, int]:
        """
        Symmetric/Affine Min-Max Quantization to signed 8-bit integers [-128, 127].
        Returns: (quantized_int8_array, scale, zero_point)
        """
        if not data:
            return array.array('b', []), 1.0, 0

        min_val = min(data)
        max_val = max(data)

        if min_val == max_val:
            scale = 1.0
            zero_point = 0
            q_data = array.array('b', [0] * len(data))
            return q_data, scale, zero_point

        # Affine scale calculation
        scale = (max_val - min_val) / 255.0
        zero_point = int(round(-min_val / scale)) - 128
        zero_point = max(-128, min(127, zero_point))

        q_list = []
        for x in data:
            q_val = int(round(x / scale)) + zero_point
            q_val = max(-128, min(127, q_val))
            q_list.append(q_val)

        return array.array('b', q_list), scale, zero_point

    @staticmethod
    def dequantize_int8_to_f64(q_data: array.array, scale: float, zero_point: int) -> List[float]:
        """
        Reconstitutes floating-point representations from INT8 compressed buffer.
        """
        return [float((q - zero_point) * scale) for q in q_data]

    @staticmethod
    def quantized_int8_vector_dot(
        q_a: array.array, scale_a: float, zp_a: int,
        q_b: array.array, scale_b: float, zp_b: int
    ) -> float:
        """
        Computes high-speed dot product entirely in integer domain,
        scaling only the final scalar accumulator.
        """
        n = len(q_a)
        acc_integer = 0
        
        for i in range(n):
            acc_integer += (q_a[i] - zp_a) * (q_b[i] - zp_b)

        return float(acc_integer * (scale_a * scale_b))

    @staticmethod
    def benchmark_compression_efficiency(elements_count: int = 10000) -> Dict[str, Any]:
        """
        Evaluates precision retention and memory reduction ratio.
        """
        raw_float_data = [math.sin(float(i) * 0.05) * 10.0 for i in range(elements_count)]
        
        q_buf, scale, zp = QuantizedTensorCore.quantize_f64_to_int8(raw_float_data)
        reconstructed = QuantizedTensorCore.dequantize_int8_to_f64(q_buf, scale, zp)

        # Calculate Mean Squared Quantization Error (MSQE)
        msqe = sum((o - r) ** 2 for o, r in zip(raw_float_data, reconstructed)) / elements_count

        raw_memory_bytes = elements_count * 8  # float64 = 8 bytes
        quantized_memory_bytes = elements_count * 1  # int8 = 1 byte

        return {
            "elements_processed": elements_count,
            "raw_f64_bytes": raw_memory_bytes,
            "quantized_int8_bytes": quantized_memory_bytes,
            "compression_ratio": f"{raw_memory_bytes / quantized_memory_bytes:.1f}x",
            "mean_squared_quantization_error": round(msqe, 6),
            "quantization_status": "HIGH_PRECISION_INT8_ACTIVE"
        }
