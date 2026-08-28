import math

class SolidStateCore:
    """Crystallography, Debye Specific Heat & Fermi Gas Dynamics"""

    H_BAR = 1.054571817e-34
    M_E = 9.10938356e-31
    K_B = 1.380649e-23
    EV_JOULE = 1.602176634e-19

    @staticmethod
    def bragg_diffraction_angle(order_n: int, wavelength_m: float, d_spacing_m: float) -> dict:
        """
        Computes Bragg angle theta for constructive crystal diffraction:
        sin(theta) = (n * lambda) / (2 * d)
        """
        if order_n <= 0 or wavelength_m <= 0 or d_spacing_m <= 0:
            raise ValueError("Parameters must be strictly positive.")

        sin_val = (order_n * wavelength_m) / (2.0 * d_spacing_m)
        if sin_val > 1.0:
            raise ValueError("Diffraction condition impossible: sin(theta) > 1.")

        theta_rad = math.asin(sin_val)
        return {
            "diffraction_order_n": order_n,
            "bragg_angle_radians": round(theta_rad, 6),
            "bragg_angle_degrees": round(math.degrees(theta_rad), 4)
        }

    @staticmethod
    def fermi_energy_free_electron(carrier_density_m3: float) -> dict:
        """
        Calculates Fermi energy E_F and Fermi wavevector k_F for 3D electron gas:
        k_F = (3 * pi^2 * n)^(1/3)
        E_F = (hbar^2 * k_F^2) / (2 * m_e)
        """
        if carrier_density_m3 <= 0:
            raise ValueError("Carrier density must be positive.")

        hbar = SolidStateCore.H_BAR
        me = SolidStateCore.M_E

        k_f = (3.0 * (math.pi ** 2) * carrier_density_m3) ** (1.0 / 3.0)
        e_f_joules = ((hbar ** 2) * (k_f ** 2)) / (2.0 * me)
        e_f_ev = e_f_joules / SolidStateCore.EV_JOULE

        return {
            "carrier_density_m3": carrier_density_m3,
            "fermi_wavevector_inv_m": f"{k_f:.6e}",
            "fermi_energy_eV": round(e_f_ev, 4),
            "fermi_energy_Joules": f"{e_f_joules:.6e}"
        }
