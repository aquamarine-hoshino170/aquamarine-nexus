import math
from typing import List, Tuple, Dict, Any
from aquamarine_nexus.core.sovereign_tensor_engine import Tensor, Linear

class SovereignGNNLayer:
    """
    Zero-Dependency Message Passing Graph Neural Network (MPNN) Layer.
    Implements permutation-invariant neighborhood feature aggregation:
    h_v^(t+1) = Update(h_v^(t), Aggregate({Message(h_u^(t), h_v^(t), e_uv) : u in N(v)}))
    """
    def __init__(self, in_features: int, out_features: int):
        self.in_features = in_features
        self.out_features = out_features
        self.w_msg = Linear(in_features, out_features)
        self.w_self = Linear(in_features, out_features)

    def forward(self, node_features: Tensor, adjacency_list: List[Tuple[int, int]]) -> Tensor:
        """
        node_features shape: (num_nodes, in_features)
        adjacency_list: [(src_node, dst_node), ...]
        """
        num_nodes = node_features.shape[0]
        
        # 1. Self projection
        self_projected = self.w_self(node_features) # (num_nodes, out_features)

        # 2. Compute neighbor message transformations
        msg_projected = self.w_msg(node_features) # (num_nodes, out_features)

        # 3. Message Aggregation (Sum Pooling)
        aggregated_messages = [[0.0] * self.out_features for _ in range(num_nodes)]
        degree_counts = [0] * num_nodes

        for src, dst in adjacency_list:
            src_msg = msg_projected.data[src * self.out_features : (src + 1) * self.out_features]
            for d in range(self.out_features):
                aggregated_messages[dst][d] += src_msg[d]
            degree_counts[dst] += 1

        # Symmetric Mean normalization
        for node_idx in range(num_nodes):
            deg = max(1, degree_counts[node_idx])
            for d in range(self.out_features):
                aggregated_messages[node_idx][d] /= float(deg)

        # 4. Combine self + aggregated neighbor messages
        agg_tensor = Tensor(aggregated_messages)
        agg_tensor.shape = (num_nodes, self.out_features)

        out = (self_projected + agg_tensor).relu()
        return out

    def parameters(self) -> List[Tensor]:
        return self.w_msg.parameters() + self.w_self.parameters()
