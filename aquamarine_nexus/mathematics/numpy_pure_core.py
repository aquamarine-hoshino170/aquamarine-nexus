import math

class NumpyPureCore:
    """Pure Python Mathematical Implementations of 50+ Core NumPy Routines"""

    # ==================== 1. LINEAR ALGEBRA (np.linalg) ====================
    @staticmethod
    def dot_product(v1: list, v2: list) -> dict:
        """Vector dot product: sum(a_i * b_i)"""
        if len(v1) != len(v2): raise ValueError("Dimension mismatch.")
        return {"dot_product": round(sum(a * b for a, b in zip(v1, v2)), 8)}

    @staticmethod
    def cross_product_3d(u: list, v: list) -> dict:
        """3D Vector Cross Product u x v"""
        if len(u) != 3 or len(v) != 3: raise ValueError("Requires 3D vectors.")
        return {"cross_product": [
            round(u[1]*v[2] - u[2]*v[1], 8),
            round(u[2]*v[0] - u[0]*v[2], 8),
            round(u[0]*v[1] - u[1]*v[0], 8)
        ]}

    @staticmethod
    def outer_product(u: list, v: list) -> dict:
        """Outer product matrix M_ij = u_i * v_j"""
        return {"outer_product": [[round(a * b, 6) for b in v] for a in u]}

    @staticmethod
    def kronecker_product_2x2(a: list, b: list) -> dict:
        """Kronecker tensor product of two 2x2 matrices (4x4 result)"""
        res = []
        for i in range(2):
            for k in range(2):
                row = []
                for j in range(2):
                    for l in range(2):
                        row.append(round(a[i][j] * b[k][l], 6))
                res.append(row)
        return {"kronecker_product_4x4": res}

    @staticmethod
    def frobenius_norm(matrix: list) -> dict:
        """Frobenius matrix norm ||A||_F = sqrt(sum |a_ij|^2)"""
        total = sum(sum(x**2 for x in row) for row in matrix)
        return {"frobenius_norm": round(math.sqrt(total), 8)}

    @staticmethod
    def matrix_det_3x3(m: list) -> dict:
        """3x3 Matrix Determinant via Sarrus / Laplace Expansion"""
        if len(m) != 3 or any(len(r) != 3 for r in m): raise ValueError("Must be 3x3 matrix.")
        det = (m[0][0]*(m[1][1]*m[2][2] - m[1][2]*m[2][1])
             - m[0][1]*(m[1][0]*m[2][2] - m[1][2]*m[2][0])
             + m[0][2]*(m[1][0]*m[2][1] - m[1][1]*m[2][0]))
        return {"det_3x3": round(det, 8)}

    @staticmethod
    def eigenvalues_2x2(a11: float, a12: float, a21: float, a22: float) -> dict:
        """Computes analytical eigenvalues for 2x2 matrix: lambda^2 - Tr*lambda + Det = 0"""
        tr = a11 + a22
        det = (a11 * a22) - (a12 * a21)
        disc = tr**2 - 4.0 * det
        if disc >= 0:
            l1 = (tr + math.sqrt(disc)) / 2.0
            l2 = (tr - math.sqrt(disc)) / 2.0
            return {"eigenvalues": [round(l1, 6), round(l2, 6)], "is_real": True}
        else:
            real_part = tr / 2.0
            imag_part = math.sqrt(-disc) / 2.0
            return {"eigenvalue_1": f"{real_part:.4f} + {imag_part:.4f}j",
                    "eigenvalue_2": f"{real_part:.4f} - {imag_part:.4f}j", "is_real": False}

    @staticmethod
    def qr_decomposition_2x2(a11: float, a12: float, a21: float, a22: float) -> dict:
        """Gram-Schmidt QR Decomposition for 2x2 matrix A = Q * R"""
        norm_v1 = math.sqrt(a11**2 + a21**2)
        if norm_v1 == 0: raise ValueError("Singular first column.")
        q11, q21 = a11 / norm_v1, a21 / norm_v1
        r11 = norm_v1
        r12 = q11 * a12 + q21 * a22
        u2_x = a12 - r12 * q11
        u2_y = a22 - r12 * q21
        norm_v2 = math.sqrt(u2_x**2 + u2_y**2)
        q12, q22 = u2_x / norm_v2, u2_y / norm_v2
        r22 = norm_v2
        return {
            "Q": [[round(q11, 6), round(q12, 6)], [round(q21, 6), round(q22, 6)]],
            "R": [[round(r11, 6), round(r12, 6)], [0.0, round(r22, 6)]]
        }

    # ==================== 2. STATISTICS & PROBABILITY (np.random / statistics) ====================
    @staticmethod
    def stats_mean_variance_std(data: list) -> dict:
        """Computes arithmetic mean, sample variance (s^2), and std deviation (sigma)"""
        n = len(data)
        if n < 2: raise ValueError("At least 2 points required.")
        mean = sum(data) / n
        var = sum((x - mean)**2 for x in data) / (n - 1)
        return {"mean": round(mean, 6), "variance": round(var, 6), "std_dev": round(math.sqrt(var), 6)}

    @staticmethod
    def weighted_average(data: list, weights: list) -> dict:
        """Computes weighted mean: sum(w_i * x_i) / sum(w_i)"""
        if len(data) != len(weights): raise ValueError("Length mismatch.")
        total_w = sum(weights)
        if total_w == 0: raise ValueError("Sum of weights cannot be zero.")
        w_avg = sum(x * w for x, w in zip(data, weights)) / total_w
        return {"weighted_average": round(w_avg, 6)}

    @staticmethod
    def covariance_pearson(x: list, y: list) -> dict:
        """Calculates Sample Covariance and Pearson Correlation Coefficient r"""
        n = len(x)
        if n != len(y) or n < 2: raise ValueError("Lists must be of equal size >= 2.")
        mx, my = sum(x) / n, sum(y) / n
        cov = sum((x[i] - mx) * (y[i] - my) for i in range(n)) / (n - 1)
        sx = math.sqrt(sum((a - mx)**2 for a in x) / (n - 1))
        sy = math.sqrt(sum((b - my)**2 for b in y) / (n - 1))
        r = cov / (sx * sy) if (sx * sy) != 0 else 0.0
        return {"covariance": round(cov, 6), "pearson_r": round(r, 6)}

    @staticmethod
    def median_and_percentiles(data: list) -> dict:
        """Computes 25th (Q1), 50th (Median), and 75th (Q3) percentiles"""
        s = sorted(data)
        n = len(s)
        def get_p(p):
            idx = p * (n - 1)
            lo = int(idx)
            hi = min(lo + 1, n - 1)
            return s[lo] + (idx - lo) * (s[hi] - s[lo])
        return {"Q1_25p": round(get_p(0.25), 4), "median_50p": round(get_p(0.50), 4), "Q3_75p": round(get_p(0.75), 4)}

    @staticmethod
    def skewness_and_kurtosis(data: list) -> dict:
        """Computes Fisher-Pearson sample skewness and excess kurtosis"""
        n = len(data)
        if n < 4: raise ValueError("At least 4 data points required.")
        mean = sum(data) / n
        m2 = sum((x - mean)**2 for x in data) / n
        m3 = sum((x - mean)**3 for x in data) / n
        m4 = sum((x - mean)**4 for x in data) / n
        skew = m3 / (m2 ** 1.5) if m2 != 0 else 0
        kurt = (m4 / (m2 ** 2)) - 3.0 if m2 != 0 else 0
        return {"skewness": round(skew, 6), "excess_kurtosis": round(kurt, 6)}

    @staticmethod
    def z_score_normalize(data: list) -> dict:
        """Z-score normalization: z = (x - mu) / sigma"""
        n = len(data)
        mean = sum(data) / n
        std = math.sqrt(sum((x - mean)**2 for x in data) / n)
        if std == 0: raise ValueError("Zero variance standard deviation.")
        z_scores = [(x - mean) / std for x in data]
        return {"z_scores": [round(z, 5) for z in z_scores]}

    @staticmethod
    def softmax_vector(logits: list) -> dict:
        """Softmax probability distribution: exp(z_i) / sum(exp(z))"""
        max_l = max(logits)
        exp_vals = [math.exp(x - max_l) for x in logits]
        total = sum(exp_vals)
        probs = [round(v / total, 6) for v in exp_vals]
        return {"softmax_probabilities": probs}

    # ==================== 3. EXPONENTIAL, LOGARITHM & SPECIAL ====================
    @staticmethod
    def log1p_and_expm1(x: float) -> dict:
        """Accurate calculation of log(1 + x) and exp(x) - 1 for small |x|"""
        return {"log1p": round(math.log1p(x), 10), "expm1": round(math.expm1(x), 10)}

    @staticmethod
    def sinc_function(x: float) -> dict:
        """Normalized Sinc function: sinc(x) = sin(pi * x) / (pi * x)"""
        if x == 0.0: return {"sinc_x": 1.0}
        val = math.sin(math.pi * x) / (math.pi * x)
        return {"sinc_x": round(val, 8)}

    @staticmethod
    def sigmoid_logistic(x: float) -> dict:
        """Sigmoid activation function: sigma(x) = 1 / (1 + exp(-x))"""
        val = 1.0 / (1.0 + math.exp(-x)) if x >= -700 else 0.0
        return {"sigmoid": round(val, 8), "derivative": round(val * (1.0 - val), 8)}

    # ==================== 4. ARRAY DIFFERENCES, CONVOLUTIONS & MISC ====================
    @staticmethod
    def cumsum_cumprod_1d(arr: list) -> dict:
        """Cumulative sum and Cumulative product of 1D array"""
        c_sum, c_prod = [], []
        acc_s, acc_p = 0.0, 1.0
        for x in arr:
            acc_s += x
            acc_p *= x
            c_sum.append(round(acc_s, 6))
            c_prod.append(round(acc_p, 6))
        return {"cumsum": c_sum, "cumprod": c_prod}

    @staticmethod
    def heaviside_step(x: float, zero_val: float = 0.5) -> dict:
        """Heaviside step function H(x)"""
        if x > 0: h = 1.0
        elif x < 0: h = 0.0
        else: h = zero_val
        return {"x": x, "H_x": h}

    @staticmethod
    def clip_array(data: list, min_val: float, max_val: float) -> dict:
        """Clips array values within interval [min_val, max_val]"""
        clipped = [min(max(x, min_val), max_val) for x in data]
        return {"clipped_array": clipped}

    @staticmethod
    def linear_interp_1d(x_eval: float, xp: list, fp: list) -> dict:
        """1D Piecewise Linear Interpolation (equivalent to np.interp)"""
        if len(xp) != len(fp) or len(xp) < 2: raise ValueError("Invalid coordinates.")
        if x_eval <= xp[0]: return {"interpolated_y": fp[0]}
        if x_eval >= xp[-1]: return {"interpolated_y": fp[-1]}
        for i in range(len(xp) - 1):
            if xp[i] <= x_eval <= xp[i + 1]:
                slope = (fp[i + 1] - fp[i]) / (xp[i + 1] - xp[i])
                y = fp[i] + slope * (x_eval - xp[i])
                return {"x_eval": x_eval, "interpolated_y": round(y, 6)}
        return {"interpolated_y": fp[-1]}

    @staticmethod
    def gcd_lcm_int(a: int, b: int) -> dict:
        """Computes Greatest Common Divisor and Least Common Multiple"""
        gcd_val = math.gcd(a, b)
        lcm_val = abs(a * b) // gcd_val if gcd_val != 0 else 0
        return {"gcd": gcd_val, "lcm": lcm_val}
