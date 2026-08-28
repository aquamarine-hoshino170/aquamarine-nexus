class GraphNetworkCore:
    @staticmethod
    def node_degree_centrality(adjacency_matrix: list) -> dict:
        """C_d(v) = deg(v) / (N - 1)"""
        n = len(adjacency_matrix)
        if n < 2 or any(len(r) != n for r in adjacency_matrix): raise ValueError("Valid square matrix >= 2 nodes required.")
        centralities = []
        for i in range(n):
            deg = sum(1 for j in range(n) if adjacency_matrix[i][j] != 0 and i != j)
            centralities.append(round(deg / (n - 1), 4))
        return {"total_nodes": n, "degree_centralities": centralities}

    @staticmethod
    def local_clustering_coefficient(adjacency_matrix: list, node_index: int) -> dict:
        """C_i = 2 * e_i / (k_i * (k_i - 1))"""
        n = len(adjacency_matrix)
        if node_index < 0 or node_index >= n: raise ValueError("Invalid node index.")
        neighbors = [j for j in range(n) if adjacency_matrix[node_index][j] != 0 and j != node_index]
        k = len(neighbors)
        if k < 2: return {"node": node_index, "degree": k, "clustering_coefficient": 0.0}
        edges_between = sum(1 for i in range(k) for j in range(i + 1, k) if adjacency_matrix[neighbors[i]][neighbors[j]] != 0)
        c_i = (2.0 * edges_between) / (k * (k - 1))
        return {"node": node_index, "degree": k, "clustering_coefficient": round(c_i, 4)}
