import math

class NexusGraph:
    """Topological Graph Theory & Network Analysis (NetworkX Alternative)"""
    @staticmethod
    def dijkstra_shortest_path(nodes: list, edges: list, start_node, target_node) -> dict:
        """Computes shortest path on weighted graph: edges = [(u, v, weight), ...]"""
        adj = {node: {} for node in nodes}
        for u, v, w in edges:
            adj[u][v] = w
            adj[v][u] = w

        distances = {node: float('inf') for node in nodes}
        distances[start_node] = 0.0
        unvisited = set(nodes)
        predecessors = {}

        while unvisited:
            curr = min(unvisited, key=lambda node: distances[node])
            if distances[curr] == float('inf') or curr == target_node:
                break
            unvisited.remove(curr)

            for neighbor, weight in adj[curr].items():
                if neighbor in unvisited:
                    new_dist = distances[curr] + weight
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        predecessors[neighbor] = curr

        # Path reconstruction
        path = []
        step = target_node
        if step in predecessors or step == start_node:
            while step is not None:
                path.append(step)
                step = predecessors.get(step)
            path.reverse()

        return {"shortest_distance": round(distances[target_node], 4), "path": path}

    @staticmethod
    def graph_laplacian_spectrum_2x2(deg_matrix: list, adj_matrix: list) -> list:
        """Computes Graph Laplacian L = D - A for 2x2 graph"""
        L = [
            [deg_matrix[0][0] - adj_matrix[0][0], deg_matrix[0][1] - adj_matrix[0][1]],
            [deg_matrix[1][0] - adj_matrix[1][0], deg_matrix[1][1] - adj_matrix[1][1]]
        ]
        # Trace and determinant for eigenvalues
        tr = L[0][0] + L[1][1]
        det = L[0][0] * L[1][1] - L[0][1] * L[1][0]
        eig1 = 0.5 * (tr + math.sqrt(max(0.0, tr**2 - 4.0 * det)))
        eig2 = 0.5 * (tr - math.sqrt(max(0.0, tr**2 - 4.0 * det)))
        return [round(eig2, 4), round(eig1, 4)]
