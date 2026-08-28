class SpectralTheoryCore:
    @staticmethod
    def gershgorin_discs_3x3(matrix_3x3: list) -> dict:
        """Gershgorin Circle Theorem: Eigenvalues lie within union of discs D(a_ii, sum_{j!=i} |a_ij|)"""
        if len(matrix_3x3) != 3 or any(len(r) != 3 for r in matrix_3x3):
            raise ValueError("Must be a 3x3 matrix.")
        discs = []
        for i in range(3):
            center = matrix_3x3[i][i]
            radius = sum(abs(matrix_3x3[i][j]) for j in range(3) if j != i)
            discs.append({"center": round(center, 4), "radius": round(radius, 4), "interval": [round(center - radius, 4), round(center + radius, 4)]})
        return {"gershgorin_discs": discs}

    @staticmethod
    def rayleigh_quotient_vector(matrix_3x3: list, vector_x: list) -> dict:
        """R(A, x) = (x^T * A * x) / (x^T * x)"""
        if len(vector_x) != 3 or len(matrix_3x3) != 3:
            raise ValueError("Matrix and vector must be 3-dimensional.")
        norm_sq = sum(x**2 for x in vector_x)
        if norm_sq == 0:
            raise ValueError("Vector cannot be zero vector.")
        ax = [sum(matrix_3x3[i][j] * vector_x[j] for j in range(3)) for i in range(3)]
        x_ax = sum(vector_x[i] * ax[i] for i in range(3))
        rq = x_ax / norm_sq
        return {"rayleigh_quotient": round(rq, 6)}
