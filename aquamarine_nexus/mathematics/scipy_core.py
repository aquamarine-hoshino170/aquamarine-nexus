import math

class NexusSciPy:
    """Numerical Optimization, Root Finding & Signal Core (SciPy Alternative)"""
    @staticmethod
    def golden_section_minimize(func, a: float, b: float, tol: float = 1e-6) -> dict:
        """Golden-section search for 1D scalar function minimization on [a, b]"""
        phi = (1.0 + math.sqrt(5.0)) / 2.0
        resphi = 2.0 - phi
        c = a + resphi * (b - a)
        d = b - resphi * (b - a)
        fc = func(c)
        fd = func(d)
        
        while abs(b - a) > tol:
            if fc < fd:
                b = d
                d = c
                fd = fc
                c = a + resphi * (b - a)
                fc = func(c)
            else:
                a = c
                c = d
                fc = fd
                d = b - resphi * (b - a)
                fd = func(d)
        xmin = (a + b) / 2.0
        return {"min_x": round(xmin, 6), "min_val": round(func(xmin), 6)}

    @staticmethod
    def discrete_convolve_1d(signal: list, kernel: list) -> list:
        """1D Discrete Linear Convolution (y = x * h)"""
        n, m = len(signal), len(kernel)
        out_len = n + m - 1
        y = [0.0] * out_len
        for i in range(out_len):
            s = 0.0
            for j in range(m):
                if 0 <= i - j < n:
                    s += signal[i - j] * kernel[j]
            y[i] = round(s, 4)
        return y
