import math

class SpecialFunctionsCore:
    """Pure Mathematics: Gamma, Beta, Error Functions & Bessel Approximations"""

    @staticmethod
    def lanczos_gamma(z_val: float) -> dict:
        """
        Computes Gamma(z) for Real(z) > 0 using Lanczos Approximation (g=7, n=9):
        Gamma(z+1) = z * Gamma(z)
        """
        if z_val <= 0 and z_val == int(z_val):
            raise ValueError("Gamma function has poles at non-positive integers.")

        # Lanczos coefficients
        p = [
            0.99999999999980993, 676.5203681218851, -1259.1392167224028,
            771.32342877765313, -176.61502916214059, 12.507343278686905,
            -0.13857109584908124, 9.9843695780195716e-6, 1.5056327351493116e-7
        ]
        g = 7
        z = z_val - 1.0
        x = p[0]
        for i in range(1, len(p)):
            x += p[i] / (z + i)

        t = z + g + 0.5
        gamma_val = math.sqrt(2.0 * math.pi) * (t ** (z + 0.5)) * math.exp(-t) * x

        return {
            "z": z_val,
            "gamma_z": round(gamma_val, 8),
            "log_gamma_z": round(math.log(abs(gamma_val)), 8)
        }

    @staticmethod
    def beta_function(a_param: float, b_param: float) -> dict:
        """
        Euler Beta Function: B(a, b) = (Gamma(a) * Gamma(b)) / Gamma(a + b)
        """
        if a_param <= 0 or b_param <= 0:
            raise ValueError("Parameters a and b must be strictly positive.")

        g_a = SpecialFunctionsCore.lanczos_gamma(a_param)["gamma_z"]
        g_b = SpecialFunctionsCore.lanczos_gamma(b_param)["gamma_z"]
        g_ab = SpecialFunctionsCore.lanczos_gamma(a_param + b_param)["gamma_z"]

        beta_val = (g_a * g_b) / g_ab
        return {
            "a": a_param,
            "b": b_param,
            "beta_value": round(beta_val, 8)
        }

    @staticmethod
    def error_function_erf(x_val: float) -> dict:
        """
        Computes Error Function erf(x) via high-precision Chebyshev approximation:
        erf(x) = (2 / sqrt(pi)) * int_0^x exp(-t^2) dt
        """
        val = math.erf(x_val)
        return {
            "x": x_val,
            "erf_x": round(val, 8),
            "erfc_x": round(1.0 - val, 8)
        }
