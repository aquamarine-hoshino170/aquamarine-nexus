class SimplicialComplexCore:
    @staticmethod
    def simplicial_euler_characteristic(simplices_count_by_dim: list) -> dict:
        """chi = sum_{k=0}^d (-1)^k * c_k (where c_k is number of k-simplices)"""
        if not simplices_count_by_dim:
            raise ValueError("Simplices array cannot be empty.")
        chi = sum(((-1) ** k) * count for k, count in enumerate(simplices_count_by_dim))
        return {
            "simplices_per_dimension": simplices_count_by_dim,
            "simplicial_euler_characteristic": chi
        }

    @staticmethod
    def discrete_laplacian_0d(degree_vector: list, adjacency_matrix: list) -> dict:
        """L = D - A"""
        n = len(degree_vector)
        if len(adjacency_matrix) != n or any(len(r) != n for r in adjacency_matrix):
            raise ValueError("Dimension mismatch.")
        laplacian = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    laplacian[i][j] = degree_vector[i] - adjacency_matrix[i][j]
                else:
                    laplacian[i][j] = -adjacency_matrix[i][j]
        return {"laplacian_matrix": laplacian}
