import math
from typing import List, Tuple

class SovereignMambaSSM:
    """
    Zero-Dependency Linear-Time State-Space Sequence Model (SSM).
    Continuous Formulation:
        h'(t) = A h(t) + B x(t)
        y(t)  = C h(t) + D x(t)
    Discretization (Zero-Order Hold / Bilinear Euler):
        \bar{A} = exp(delta * A)
        \bar{B} = (delta * A)^(-1) * (\bar{A} - I) * (delta * B) \approx delta * B
        h_t     = \bar{A} h_{t-1} + \bar{B} x_t
        y_t     = C h_t + D x_t
    Complexity: O(L) Time, O(1) Memory per step (Eliminates O(L^2) Attention Bottleneck).
    """
    def __init__(self, d_model: int = 4, d_state: int = 8, delta: float = 0.1):
        self.d_model = d_model
        self.d_state = d_state
        self.delta = delta

        # HiPPO-inspired continuous state transition matrix A (Strictly negative diagonal for stability)
        self.A = [[-0.5 * (1.0 + (p == q)) for q in range(d_state)] for p in range(d_state)]

        # Input projection B: (d_state, d_model)
        scale_b = 1.0 / math.sqrt(d_model)
        self.B = [[0.1 * ((i + j) % 3) * scale_b for j in range(d_model)] for i in range(d_state)]

        # Output projection C: (d_model, d_state)
        scale_c = 1.0 / math.sqrt(d_state)
        self.C = [[0.1 * ((i - j) % 3) * scale_c for j in range(d_state)] for i in range(d_model)]

        # Direct feedthrough D: (d_model)
        self.D = [1.0] * d_model

        # Precompute discretized \bar{A} and \bar{B}
        self.A_bar = self._discretize_a()

    def _discretize_a(self) -> List[List[float]]:
        """Computes Taylor expansion approximation of exp(delta * A)."""
        A_bar = [[0.0] * self.d_state for _ in range(self.d_state)]
        for i in range(self.d_state):
            for j in range(self.d_state):
                identity = 1.0 if i == j else 0.0
                A_bar[i][j] = identity + self.delta * self.A[i][j]
        return A_bar

    def forward_sequence(self, x_seq: List[List[float]]) -> List[List[float]]:
        """
        Processes entire sequence of length L in linear O(L) complexity.
        x_seq: Shape (seq_len, d_model) -> Output: Shape (seq_len, d_model)
        """
        seq_len = len(x_seq)
        y_seq = []

        # Hidden state buffer: Shape (d_state)
        h = [0.0] * self.d_state

        for t in range(seq_len):
            x_t = x_seq[t]

            # 1. State update: h_next = A_bar @ h + B_bar @ x_t
            h_next = [0.0] * self.d_state
            for i in range(self.d_state):
                # State transition term
                state_term = sum(self.A_bar[i][j] * h[j] for j in range(self.d_state))
                # Input excitation term (delta * B @ x_t)
                input_term = self.delta * sum(self.B[i][k] * x_t[k] for k in range(self.d_model))
                h_next[i] = state_term + input_term

            h = h_next

            # 2. Output projection: y_t = C @ h + D * x_t
            y_t = [0.0] * self.d_model
            for m in range(self.d_model):
                proj_term = sum(self.C[m][i] * h[i] for i in range(self.d_state))
                skip_term = self.D[m] * x_t[m]
                y_t[m] = proj_term + skip_term

            y_seq.append(y_t)

        return y_seq
