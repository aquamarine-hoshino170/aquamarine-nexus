class DeRhamCohomologyCore:
    @staticmethod
    def manifold_betti_numbers_invariants(dim_n: int, betti_list: list) -> dict:
        """Euler characteristic chi = sum_{k=0}^n (-1)^k * b_k, Poincaré Duality: b_k = b_{n-k} for closed orientable manifolds"""
        if len(betti_list) != (dim_n + 1):
            raise ValueError("Betti numbers list length must be dim + 1 (from b_0 to b_n).")
            
        chi = sum(((-1) ** k) * b for k, b in enumerate(betti_list))
        
        # Verify Poincaré Duality symmetry: b_k == b_{n-k}
        is_poincare_dual = all(betti_list[k] == betti_list[dim_n - k] for k in range(dim_n + 1))
        
        return {
            "manifold_dimension_n": dim_n,
            "betti_numbers": betti_list,
            "computed_euler_characteristic_chi": chi,
            "satisfies_poincare_duality": is_poincare_dual,
            "orientability_classification": "Closed Orientable Manifold" if is_poincare_dual else "Non-orientable / Boundary Manifold"
        }
