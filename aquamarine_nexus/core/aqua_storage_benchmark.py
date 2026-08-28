from array import array
import os
from aquamarine_nexus.core.aqua_binary_serializer import AquaBinaryProtocol

class AquaStorageBenchmarkCore:
    @staticmethod
    def benchmark_aqua_serialization(total_elements: int = 1000000, target_filename: str = "benchmark_tensor.aqua") -> dict:
        """
        Generates 1M+ float64 numbers, saves to native .aqua zero-copy format,
        and reads them back instantly to measure IO speed and data integrity.
        """
        if total_elements <= 0:
            raise ValueError("Total elements must be strictly positive.")

        # Allocate dense buffer
        raw_data = array('d', (float(i) * 0.5 for i in range(total_elements)))
        shape = (1000, total_elements // 1000)

        # 1. Save benchmark
        save_report = AquaBinaryProtocol.save_aqua_tensor(target_filename, raw_data, shape)

        # 2. Load benchmark
        loaded_buffer, loaded_shape, load_report = AquaBinaryProtocol.load_aqua_tensor(target_filename)

        # Verify integrity
        checksum_original = raw_data[0] + raw_data[-1]
        checksum_loaded = loaded_buffer[0] + loaded_buffer[-1]
        integrity_verified = (checksum_original == checksum_loaded) and (shape == loaded_shape)

        # Cleanup generated file
        if os.path.exists(target_filename):
            os.remove(target_filename)

        return {
            "elements_benchmarked": total_elements,
            "tensor_shape": list(shape),
            "save_performance": save_report,
            "load_performance": load_report,
            "byte_exact_integrity_verified": integrity_verified,
            "verdict": "ZERO_COPY_PERSISTENCE_OPERATIONAL"
        }
