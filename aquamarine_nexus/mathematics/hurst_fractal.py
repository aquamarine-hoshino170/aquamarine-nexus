import math

class HurstFractalCore:
    @staticmethod
    def rescaled_range_step(time_series: list) -> dict:
        """R/S = (max(Y_t) - min(Y_t)) / S"""
        n = len(time_series)
        if n < 4:
            raise ValueError("At least 4 data points required.")
        mean_val = sum(time_series) / n
        centered = [x - mean_val for x in time_series]
        
        # Cumulative deviations
        y = []
        acc = 0.0
        for c in centered:
            acc += c
            y.append(acc)
            
        r_range = max(y) - min(y)
        std_s = math.sqrt(sum(c**2 for c in centered) / n)
        if std_s == 0:
            raise ValueError("Zero standard deviation.")
            
        rs_stat = r_range / std_s
        # Hurst proxy: H approx log(R/S) / log(n)
        h_approx = math.log(rs_stat) / math.log(n)
        
        nature = "Persistent / Long-Memory (H > 0.5)" if h_approx > 0.55 else (
            "Anti-persistent / Mean-Reverting (H < 0.5)" if h_approx < 0.45 else "Random Walk / Brownian (H approx 0.5)"
        )
        return {
            "n_samples": n,
            "range_R": round(r_range, 6),
            "std_dev_S": round(std_s, 6),
            "rescaled_range_RS": round(rs_stat, 6),
            "hurst_exponent_proxy": round(min(max(h_approx, 0.0), 1.0), 4),
            "time_series_nature": nature
        }
