import array
import threading
from typing import List, Dict, Any

class RingAllReduceNode:
    """
    Zero-Dependency Distributed Ring-AllReduce Worker Core.
    Executes optimal bandwidth gradient synchronization across N logical workers:
    Total transfer volume = 2 * ((N - 1) / N) * Vector_Size.
    """
    def __init__(self, rank: int, world_size: int):
        self.rank = rank
        self.world_size = world_size
        self.buffer: array.array = array.array('d')

    def set_gradients(self, grads: List[float]):
        self.buffer = array.array('d', grads)

class PureRingAllReduceCluster:
    """
    Simulates / Coordinates multi-node sovereign Ring-AllReduce topology.
    """
    def __init__(self, world_size: int):
        self.world_size = world_size
        self.nodes = [RingAllReduceNode(r, world_size) for r in range(world_size)]

    def synchronize(self, gradients_per_rank: List[List[float]]) -> List[List[float]]:
        N = self.world_size
        L = len(gradients_per_rank[0])
        chunk_size = L // N

        # Initialize rank buffers
        for r in range(N):
            self.nodes[r].set_gradients(gradients_per_rank[r])

        # Step 1: Scatter-Reduce Phase (N - 1 steps)
        for step in range(N - 1):
            temp_transfers = []
            for r in range(N):
                send_chunk = (r - step) % N
                recv_rank = (r + 1) % N
                # Send slice from rank r to recv_rank
                start = send_chunk * chunk_size
                end = start + chunk_size if send_chunk != N - 1 else L
                data_slice = self.nodes[r].buffer[start:end]
                temp_transfers.append((recv_rank, send_chunk, data_slice))

            # Apply partial reduction in-memory
            for recv_rank, chunk_idx, data_slice in temp_transfers:
                start = chunk_idx * chunk_size
                for i, val in enumerate(data_slice):
                    self.nodes[recv_rank].buffer[start + i] += val

        # Step 2: Allgather Phase (N - 1 steps)
        for step in range(N - 1):
            temp_transfers = []
            for r in range(N):
                send_chunk = (r - step + 1) % N
                recv_rank = (r + 1) % N
                start = send_chunk * chunk_size
                end = start + chunk_size if send_chunk != N - 1 else L
                data_slice = self.nodes[r].buffer[start:end]
                temp_transfers.append((recv_rank, send_chunk, data_slice))

            for recv_rank, chunk_idx, data_slice in temp_transfers:
                start = chunk_idx * chunk_size
                for i, val in enumerate(data_slice):
                    self.nodes[recv_rank].buffer[start + i] = val

        # Compute average (divide by world_size)
        results = []
        for r in range(N):
            avg_buf = [val / float(N) for val in self.nodes[r].buffer]
            results.append(avg_buf)

        return results
