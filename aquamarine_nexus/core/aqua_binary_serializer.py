from array import array
import struct
import time
from typing import Tuple, Dict, Any

class AquaBinaryProtocol:
    MAGIC_HEADER = b"AQUA"
    SPEC_VERSION = 1

    @staticmethod
    def save_aqua_tensor(file_path: str, data_buffer: array, shape: Tuple[int, ...]) -> Dict[str, Any]:
        """
        Saves raw memory buffer directly to disk using zero-copy binary layout.
        No JSON or text parsing overhead.
        """
        if not file_path.endswith(".aqua"):
            file_path += ".aqua"

        if not isinstance(data_buffer, array) or data_buffer.typecode != 'd':
            raise TypeError("data_buffer must be an array of typecode 'd' (float64).")

        expected_elements = 1
        for dim in shape:
            expected_elements *= dim

        if len(data_buffer) != expected_elements:
            raise ValueError(f"Shape {shape} does not match element count {len(data_buffer)}.")

        rank = len(shape)
        # Header structure: Magic (4s), Version (H), Rank (H), Dimensions (Q * Rank)
        header_fmt = f"<4sHH{rank}Q"
        header_bytes = struct.pack(header_fmt, AquaBinaryProtocol.MAGIC_HEADER, AquaBinaryProtocol.SPEC_VERSION, rank, *shape)

        t0 = time.perf_counter()
        with open(file_path, "wb") as f:
            f.write(header_bytes)
            data_buffer.tofile(f)
        write_time_sec = time.perf_counter() - t0

        file_size_bytes = len(header_bytes) + (len(data_buffer) * 8)
        throughput_mb_s = (file_size_bytes / (1024 * 1024)) / (write_time_sec + 1e-12)

        return {
            "file_path": file_path,
            "tensor_shape": list(shape),
            "total_elements": expected_elements,
            "raw_payload_bytes": len(data_buffer) * 8,
            "total_file_size_bytes": file_size_bytes,
            "write_time_seconds": round(write_time_sec, 6),
            "write_throughput_MB_per_sec": round(throughput_mb_s, 2),
            "status": "AQUA_ZERO_COPY_SAVE_SUCCESS"
        }

    @staticmethod
    def load_aqua_tensor(file_path: str) -> Tuple[array, Tuple[int, ...], Dict[str, Any]]:
        """
        Loads .aqua binary file directly into a pre-allocated memoryview buffer.
        """
        if not file_path.endswith(".aqua"):
            file_path += ".aqua"

        t0 = time.perf_counter()
        with open(file_path, "rb") as f:
            # Read magic bytes (4B), version (2B), rank (2B)
            base_header = f.read(8)
            if len(base_header) < 8:
                raise ValueError("Corrupted .aqua binary file: header too short.")

            magic, version, rank = struct.unpack("<4sHH", base_header)
            if magic != AquaBinaryProtocol.MAGIC_HEADER:
                raise ValueError(f"Invalid binary magic signature: {magic}")

            # Read dimensions
            dims_bytes = f.read(8 * rank)
            shape = struct.unpack(f"<{rank}Q", dims_bytes)

            expected_elements = 1
            for dim in shape:
                expected_elements *= dim

            # Direct buffer reading
            tensor_buffer = array('d')
            tensor_buffer.fromfile(f, expected_elements)

        read_time_sec = time.perf_counter() - t0
        file_size_bytes = 8 + (8 * rank) + (expected_elements * 8)
        throughput_mb_s = (file_size_bytes / (1024 * 1024)) / (read_time_sec + 1e-12)

        metadata = {
            "file_path": file_path,
            "spec_version": version,
            "tensor_shape": list(shape),
            "total_elements": expected_elements,
            "read_time_seconds": round(read_time_sec, 6),
            "read_throughput_MB_per_sec": round(throughput_mb_s, 2),
            "status": "AQUA_ZERO_COPY_LOAD_SUCCESS"
        }

        return tensor_buffer, shape, metadata
