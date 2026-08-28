from typing import Callable, Dict, List, Any

class CustomFormulaOp:
    """
    User-Defined Atomic Mathematical Node.
    """
    def __init__(
        self,
        name: str,
        forward_fn: Callable[[List[float]], List[float]],
        backward_fn: Callable[[List[float], List[float]], List[float]] = None
    ):
        self.name = name
        self.forward_fn = forward_fn
        # Numerical gradient fallback if backward derivative is not provided
        self.backward_fn = backward_fn or self._numerical_gradient

    def _numerical_gradient(self, inputs: List[float], grad_output: List[float], eps: float = 1e-5) -> List[float]:
        """Calculates numerical derivative via symmetric finite difference: (f(x+h) - f(x-h)) / 2h"""
        in_grads = [0.0] * len(inputs)
        base_out = self.forward_fn(inputs)
        
        for idx in range(len(inputs)):
            x_plus = list(inputs)
            x_minus = list(inputs)
            x_plus[idx] += eps
            x_minus[idx] -= eps
            
            out_plus = self.forward_fn(x_plus)
            out_minus = self.forward_fn(x_minus)
            
            # Chain rule with incoming gradient
            local_deriv = sum((out_plus[k] - out_minus[k]) / (2.0 * eps) * grad_output[k] for k in range(len(base_out)))
            in_grads[idx] = local_deriv
            
        return in_grads

class FormulaRegistry:
    """
    Global Sovereign Formula & Operator Extensibility Hub.
    """
    _registry: Dict[str, CustomFormulaOp] = {}

    @classmethod
    def register(
        cls,
        name: str,
        forward_fn: Callable[[List[float]], List[float]],
        backward_fn: Callable[[List[float], List[float]], List[float]] = None
    ):
        """Registers a user-defined formula seamlessly."""
        cls._registry[name] = CustomFormulaOp(name, forward_fn, backward_fn)

    @classmethod
    def execute(cls, name: str, inputs: List[float]) -> List[float]:
        if name not in cls._registry:
            raise KeyError(
                f"Formula '{name}' is not in core. Use FormulaRegistry.register('{name}', forward_fn) to add it dynamically."
            )
        return cls._registry[name].forward_fn(inputs)

    @classmethod
    def backprop(cls, name: str, inputs: List[float], grad_output: List[float]) -> List[float]:
        if name not in cls._registry:
            raise KeyError(f"Formula '{name}' is not registered.")
        return cls._registry[name].backward_fn(inputs, grad_output)
