class TuringMorphogenesisCore:
    """Reaction-Diffusion & Chemical Morphogenesis Engine (Gray-Scott Local State)"""

    @staticmethod
    def gray_scott_point_step(u: float, v: float, f_feed: float = 0.055, k_kill: float = 0.062, dt: float = 1.0) -> dict:
        """
        Calculates local chemical reaction for Morphogens:
        du/dt = -u*v^2 + F*(1 - u)
        dv/dt =  u*v^2 - (F + k)*v
        """
        reaction = u * (v ** 2)
        du = -reaction + f_feed * (1.0 - u)
        dv = reaction - (f_feed + k_kill) * v

        u_next = max(0.0, min(1.0, u + du * dt))
        v_next = max(0.0, min(1.0, v + dv * dt))

        return {
            "morphogen_U": round(u_next, 6),
            "morphogen_V": round(v_next, 6),
            "reaction_rate": round(reaction, 6)
        }
