import math

class NexusMLStats:
    """Statistical Learning & Machine Learning Core (Scikit-Learn/Statsmodels Alternative)"""
    @staticmethod
    def linear_regression_1d(x_vals: list, y_vals: list) -> dict:
        """Ordinary Least Squares (OLS) Linear Regression: y = m*x + c"""
        n = len(x_vals)
        if n != len(y_vals) or n < 2:
            raise ValueError("Input lists must be of the same length and have at least 2 points.")
        
        x_mean = sum(x_vals) / n
        y_mean = sum(y_vals) / n
        
        num = sum((x_vals[i] - x_mean) * (y_vals[i] - y_mean) for i in range(n))
        den = sum((x_vals[i] - x_mean) ** 2 for i in range(n))
        if den == 0:
            raise ZeroDivisionError("Cannot fit a line to vertical points.")
            
        m = num / den
        c = y_mean - m * x_mean
        
        # Calculate R^2 score
        ss_tot = sum((y - y_mean) ** 2 for y in y_vals)
        ss_res = sum((y_vals[i] - (m * x_vals[i] + c)) ** 2 for i in range(n))
        r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 1.0
        
        return {"slope_m": round(m, 5), "intercept_c": round(c, 5), "r_squared": round(r2, 5)}

    @staticmethod
    def kmeans_1d(data: list, k: int = 2, max_iters: int = 20) -> dict:
        """1D K-Means Clustering"""
        if len(data) < k:
            raise ValueError("Data points must be greater than or equal to k.")
        
        # Uniform initial centroid placement
        data_sorted = sorted(data)
        step = len(data_sorted) // k
        centroids = [data_sorted[i * step] for i in range(k)]
        
        for _ in range(max_iters):
            clusters = {i: [] for i in range(k)}
            for x in data:
                nearest_idx = min(range(k), key=lambda i: abs(x - centroids[i]))
                clusters[nearest_idx].append(x)
            
            new_centroids = []
            for i in range(k):
                if clusters[i]:
                    new_centroids.append(sum(clusters[i]) / len(clusters[i]))
                else:
                    new_centroids.append(centroids[i])
            
            if new_centroids == centroids:
                break
            centroids = new_centroids
            
        return {"centroids": [round(c, 4) for c in centroids], "cluster_counts": [len(clusters[i]) for i in range(k)]}
