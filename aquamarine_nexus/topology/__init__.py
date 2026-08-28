class PointSetTopology:
    """Topological Spaces & Closure Operators"""
    @staticmethod
    def is_valid_topology(universal_set: set, open_sets: list) -> bool:
        """Verifies if open_sets forms a valid topology on universal_set:
        1. Empty set and universal_set are in open_sets
        2. Closed under arbitrary unions
        3. Closed under finite intersections
        """
        open_set_list = [set(s) for s in open_sets]
        if set() not in open_set_list or universal_set not in open_set_list:
            return False
        
        # Check union closure
        for s1 in open_set_list:
            for s2 in open_set_list:
                if (s1 | s2) not in open_set_list:
                    return False
        
        # Check intersection closure
        for s1 in open_set_list:
            for s2 in open_set_list:
                if (s1 & s2) not in open_set_list:
                    return False
        return True

class AlgebraicTopology:
    """Simplicial Complexes, Homology & Topological Invariants"""
    @staticmethod
    def euler_characteristic(vertices: int, edges: int, faces: int) -> dict:
        """Euler-Poincaré Formula: chi = V - E + F"""
        chi = vertices - edges + faces
        genus = None
        # For closed orientable 2-manifolds: chi = 2 - 2g => g = (2 - chi)/2
        if (2 - chi) % 2 == 0:
            genus = (2 - chi) // 2
        return {"euler_characteristic": chi, "orientable_genus": genus}

    @staticmethod
    def betti_numbers_surface(genus: int, boundaries: int = 0) -> dict:
        """Betti numbers b0, b1, b2 for compact surfaces"""
        b0 = 1
        b1 = 2 * genus + max(0, boundaries - 1) if boundaries > 0 else 2 * genus
        b2 = 0 if boundaries > 0 else 1
        chi = b0 - b1 + b2
        return {"b0": b0, "b1": b1, "b2": b2, "chi": chi}
