import math

class CardiacPoincareHRVCore:
    @staticmethod
    def poincare_sd1_sd2_descriptors(rr_intervals_ms: list) -> dict:
        """SD1 = sqrt(Var(RR_n - RR_{n+1}) / 2), SD2 = sqrt(2*Var(RR_n) - Var(RR_n - RR_{n+1}) / 2)"""
        n = len(rr_intervals_ms)
        if n < 4:
            raise ValueError("At least 4 consecutive RR-intervals required.")
            
        diffs = [rr_intervals_ms[i+1] - rr_intervals_ms[i] for i in range(n - 1)]
        mean_diff = sum(diffs) / len(diffs)
        var_diff = sum((d - mean_diff) ** 2 for d in diffs) / len(diffs)
        
        sd1 = math.sqrt(var_diff / 2.0)
        
        mean_rr = sum(rr_intervals_ms) / n
        var_rr = sum((r - mean_rr) ** 2 for r in rr_intervals_ms) / n
        
        sd2_sq = max(0.0, 2.0 * var_rr - (var_diff / 2.0))
        sd2 = math.sqrt(sd2_sq)
        
        ratio = sd1 / sd2 if sd2 > 0 else 0.0
        
        return {
            "total_intervals": n,
            "sd1_parasympathetic_ms": round(sd1, 4),
            "sd2_sympathovagal_ms": round(sd2, 4),
            "sd1_sd2_ratio": round(ratio, 4),
            "autonomic_state": "Vagal Dominant" if ratio > 0.5 else "Sympathetic Accentuation"
        }
