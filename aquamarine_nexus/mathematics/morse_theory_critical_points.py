class MorseTheoryCriticalPointsCore:
    @staticmethod
    def classify_2d_morse_critical_point(hessian_xx: float, hessian_yy: float, hessian_xy: float) -> dict:
        """Det(H) = H_xx * H_yy - H_xy^2, Morse Index lambda = number of negative eigenvalues"""
        det_h = (hessian_xx * hessian_yy) - (hessian_xy ** 2)
        trace_h = hessian_xx + hessian_yy
        
        if abs(det_h) < 1e-12:
            return {
                "determinant_Hessian": 0.0,
                "is_non_degenerate_morse": False,
                "critical_classification": "Degenerate / Monkey Saddle Point (Non-Morse)"
            }
            
        # Eigenvalues via quadratic characteristic equation
        disc = ((trace_h ** 2) - (4.0 * det_h)) ** 0.5
        eig1 = 0.5 * (trace_h + disc)
        eig2 = 0.5 * (trace_h - disc)
        
        morse_index = sum(1 for eig in [eig1, eig2] if eig < 0)
        
        topology_label = "Local Minimum (Index 0)" if morse_index == 0 else ("Pass / Saddle Point (Index 1)" if morse_index == 1 else "Local Maximum (Index 2)")
        
        return {
            "eigenvalue_1": round(eig1, 6),
            "eigenvalue_2": round(eig2, 6),
            "morse_index_lambda": morse_index,
            "is_non_degenerate_morse": True,
            "critical_topology": topology_label
        }
