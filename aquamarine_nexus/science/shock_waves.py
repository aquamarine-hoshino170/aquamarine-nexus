class ShockWaveCore:
    """Compressible Fluid Dynamics & Rankine-Hugoniot Shock Relations"""

    @staticmethod
    def normal_shock_relations(mach_1: float, gamma: float = 1.4) -> dict:
        """
        Computes downstream properties across a normal shock wave given upstream Mach number M1 > 1.
        """
        if mach_1 <= 1.0:
            raise ValueError("Upstream Mach number must be supersonic (M1 > 1.0) for a shock wave.")
        
        m1_sq = mach_1 ** 2
        
        # Downstream Mach number M2
        m2_num = (gamma - 1.0) * m1_sq + 2.0
        m2_den = 2.0 * gamma * m1_sq - (gamma - 1.0)
        mach_2 = (m2_num / m2_den) ** 0.5

        # Static Pressure Ratio P2 / P1
        p_ratio = (2.0 * gamma * m1_sq - (gamma - 1.0)) / (gamma + 1.0)

        # Density Ratio rho2 / rho1
        rho_ratio = ((gamma + 1.0) * m1_sq) / ((gamma - 1.0) * m1_sq + 2.0)

        # Temperature Ratio T2 / T1
        t_ratio = p_ratio / rho_ratio

        return {
            "upstream_mach_M1": mach_1,
            "downstream_mach_M2": round(mach_2, 5),
            "pressure_ratio_P2_P1": round(p_ratio, 5),
            "density_ratio_rho2_rho1": round(rho_ratio, 5),
            "temperature_ratio_T2_T1": round(t_ratio, 5)
        }
