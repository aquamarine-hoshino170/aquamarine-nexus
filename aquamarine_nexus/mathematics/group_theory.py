class GroupTheoryCore:
    """Abstract Algebra, Symmetric Groups & Group Actions"""

    @staticmethod
    def permutation_compose(p1: list, p2: list) -> list:
        """
        Composes two permutations (p1 ∘ p2) represented as 0-indexed lists.
        Example: p1=[1, 2, 0], p2=[2, 1, 0] -> (p1 ∘ p2)[i] = p1[p2[i]]
        """
        if len(p1) != len(p2):
            raise ValueError("Permutations must have the same length.")
        return [p1[p2[i]] for i in range(len(p1))]

    @staticmethod
    def cyclic_subgroup_order(element: int, modulus: int) -> dict:
        """
        Computes the order and orbit of an element in the additive group (Z/nZ, +)
        """
        orbit = []
        curr = 0
        while True:
            curr = (curr + element) % modulus
            orbit.append(curr)
            if curr == 0:
                break
        return {"element": element, "modulus": modulus, "order": len(orbit), "orbit": orbit}
