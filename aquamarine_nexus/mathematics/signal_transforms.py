import math

class SignalTransformsCore:
    @staticmethod
    def discrete_autocovariance_1d(signal: list, max_lag: int = 5) -> dict:
        """gamma(k) = (1/N) * sum_{t=0}^{N-k-1} (x_t - mu)*(x_{t+k} - mu)"""
        n = len(signal)
        if n < 2 or max_lag >= n: raise ValueError("Invalid signal length or lag.")
        mean = sum(signal) / n
        centered = [x - mean for x in signal]
        autocov = []
        for k in range(max_lag + 1):
            gamma_k = sum(centered[t] * centered[t + k] for t in range(n - k)) / n
            autocov.append(round(gamma_k, 6))
        return {"mean": round(mean, 6), "variance_lag0": autocov[0], "autocovariance_vector": autocov}

    @staticmethod
    def wiener_snr_gain(signal_power: float, noise_power: float) -> dict:
        """H_opt = S_xx / (S_xx + S_nn) ; SNR = S_xx / S_nn"""
        if signal_power <= 0 or noise_power <= 0: raise ValueError("Powers must be strictly positive.")
        gain = signal_power / (signal_power + noise_power)
        snr = signal_power / noise_power
        snr_db = 10.0 * math.log10(snr)
        return {"snr_linear": round(snr, 4), "snr_dB": round(snr_db, 2), "optimal_wiener_filter_gain": round(gain, 6)}
