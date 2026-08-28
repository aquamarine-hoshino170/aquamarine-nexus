import math

class WaveletAnalysisCore:
    @staticmethod
    def haar_wavelet_step_1d(signal: list) -> dict:
        """1-level Discrete Haar Wavelet Transform (Approximation & Detail Coefficients)"""
        n = len(signal)
        if n % 2 != 0 or n < 2:
            raise ValueError("Signal length must be an even integer >= 2.")
        inv_sqrt2 = 1.0 / math.sqrt(2.0)
        approx = []
        detail = []
        for i in range(0, n, 2):
            a = (signal[i] + signal[i + 1]) * inv_sqrt2
            d = (signal[i] - signal[i + 1]) * inv_sqrt2
            approx.append(round(a, 6))
            detail.append(round(d, 6))
        return {
            "approximation_coeffs_cA": approx,
            "detail_coeffs_cD": detail
        }

    @staticmethod
    def morlet_wavelet_value(t_val: float, omega0: float = 5.0) -> dict:
        """psi(t) = pi^(-1/4) * exp(i * omega0 * t) * exp(-t^2 / 2)"""
        pi_factor = math.pi ** (-0.25)
        gaussian_envelope = math.exp(-(t_val ** 2) / 2.0)
        real_part = pi_factor * gaussian_envelope * math.cos(omega0 * t_val)
        imag_part = pi_factor * gaussian_envelope * math.sin(omega0 * t_val)
        return {
            "t": t_val,
            "omega0": omega0,
            "real_morlet": round(real_part, 6),
            "imag_morlet": round(imag_part, 6),
            "envelope": round(pi_factor * gaussian_envelope, 6)
        }
