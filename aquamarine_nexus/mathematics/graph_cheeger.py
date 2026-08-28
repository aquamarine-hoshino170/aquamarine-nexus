import math

class GraphCheegerCore:
    @staticmethod
    def cheeger_inequality_bounds(lambda_2_laplacian: float, max_degree_d: float) -> dict:
        """lambda_2 / 2 <= h(G) <= sqrt(2 * d * lambda_2)"""
        if lambda_2_laplacian < 0 or max_degree_d <= 0:
            raise ValueError("Spectral gap and degree must be positive.")
        
        lower_bound = lambda_2_laplacian / 2.0
        upper_bound = math.sqrt(2.0 * max_degree_d * lambda_2_laplacian)
        
        return {
            "spectral_gap_lambda2": round(lambda_2_laplacian, 6),
            "cheeger_constant_lower_bound": round(lower_bound, 6),
            "cheeger_constant_upper_bound": round(upper_bound, 6)
        }

    @staticmethod
    def expander_mixing_lemma_bound(num_edges_e: float, num_nodes_n: float, lambda_2: float, s_size: int, t_size: int) -> dict:
        """|e(S, T) - d*|S|*|T|/n| <= lambda_2 * sqrt(|S|*|T|)"""
        if num_nodes_n <= 0 or s_size <= 0 or t_size <= 0:
            raise ValueError("Invalid graph dimensions.")
        
        d_avg = (2.0 * num_edges_e) / num_nodes_n
        expected_edges = (d_avg * s_size * t_size) / num_nodes_n
        max_discrepancy = lambda_2 * math.sqrt(s_size * t_size)
        
        return {
            "expected_random_edges": round(expected_edges, 4),
            "spectral_max_discrepancy": round(max_discrepancy, 4)
        }
