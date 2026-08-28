import math
import random
from typing import List, Tuple, Union, Optional, Set, Callable

class Tensor:
    """
    Zero-Dependency Sovereign N-Dimensional Autograd Tensor.
    Fully native backpropagation engine with scalar broadcasting.
    """
    def __init__(self, data: Union[float, int, List], _children: Tuple['Tensor', ...] = (), _op: str = ''):
        if isinstance(data, (int, float)):
            self.data = [float(data)]
            self.shape = (1,)
        elif isinstance(data, list):
            self.shape = self._infer_shape(data)
            self.data = self._flatten(data)
        else:
            raise TypeError("Unsupported data type for Tensor initialization.")

        self.grad: List[float] = [0.0] * len(self.data)
        self._backward: Callable[[], None] = lambda: None
        self._prev: Set['Tensor'] = set(_children)
        self._op: str = _op

    @classmethod
    def _infer_shape(cls, nested_list: List) -> Tuple[int, ...]:
        shape = []
        curr = nested_list
        while isinstance(curr, list):
            shape.append(len(curr))
            curr = curr[0] if len(curr) > 0 else None
        return tuple(shape)

    @classmethod
    def _flatten(cls, nested_list: List) -> List[float]:
        flat = []
        def _recurse(item):
            if isinstance(item, list):
                for sub in item:
                    _recurse(sub)
            else:
                flat.append(float(item))
        _recurse(nested_list)
        return flat

    def __repr__(self) -> str:
        return f"Tensor(shape={self.shape}, data={self.data[:8]}{'...' if len(self.data) > 8 else ''})"

    def zero_grad(self):
        self.grad = [0.0] * len(self.data)

    def __add__(self, other: Union['Tensor', float, int]) -> 'Tensor':
        if isinstance(other, (int, float)):
            other = Tensor([float(other)] * len(self.data))
            other.shape = self.shape
        elif other.shape == (1,) and self.shape != (1,):
            scalar_val = other.data[0]
            other = Tensor([scalar_val] * len(self.data))
            other.shape = self.shape
        elif self.shape != other.shape:
            raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")

        out_data = [a + b for a, b in zip(self.data, other.data)]
        out = Tensor(out_data, (self, other), '+')
        out.shape = self.shape

        def _backward():
            for i in range(len(self.data)):
                self.grad[i] += 1.0 * out.grad[i]
                other.grad[i] += 1.0 * out.grad[i]
        out._backward = _backward
        return out

    def __radd__(self, other: Union[float, int]) -> 'Tensor':
        return self.__add__(other)

    def __mul__(self, other: Union['Tensor', float, int]) -> 'Tensor':
        if isinstance(other, (int, float)):
            scalar_val = float(other)
            out_data = [a * scalar_val for a in self.data]
            out = Tensor(out_data, (self,), f'*{scalar_val}')
            out.shape = self.shape

            def _backward():
                for i in range(len(self.data)):
                    self.grad[i] += scalar_val * out.grad[i]
            out._backward = _backward
            return out

        if other.shape == (1,) and self.shape != (1,):
            scalar_val = other.data[0]
            out_data = [a * scalar_val for a in self.data]
            out = Tensor(out_data, (self, other), '*')
            out.shape = self.shape

            def _backward():
                for i in range(len(self.data)):
                    self.grad[i] += scalar_val * out.grad[i]
                    other.grad[0] += self.data[i] * out.grad[i]
            out._backward = _backward
            return out

        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")

        out_data = [a * b for a, b in zip(self.data, other.data)]
        out = Tensor(out_data, (self, other), '*')
        out.shape = self.shape

        def _backward():
            for i in range(len(self.data)):
                self.grad[i] += other.data[i] * out.grad[i]
                other.grad[i] += self.data[i] * out.grad[i]
        out._backward = _backward
        return out

    def __rmul__(self, other: Union[float, int]) -> 'Tensor':
        return self.__mul__(other)

    def __sub__(self, other: Union['Tensor', float, int]) -> 'Tensor':
        if isinstance(other, (int, float)):
            return self + (-float(other))
        return self + (other * -1.0)

    def __rsub__(self, other: Union[float, int]) -> 'Tensor':
        return (self * -1.0) + other

    def matmul(self, other: 'Tensor') -> 'Tensor':
        if len(self.shape) != 2 or len(other.shape) != 2:
            raise ValueError("Matmul requires 2D tensors.")
        r1, c1 = self.shape
        r2, c2 = other.shape
        if c1 != r2:
            raise ValueError(f"Matrix dimension mismatch: {self.shape} x {other.shape}")

        out_flat = [0.0] * (r1 * c2)
        for i in range(r1):
            for k in range(c1):
                s_val = self.data[i * c1 + k]
                for j in range(c2):
                    out_flat[i * c2 + j] += s_val * other.data[k * c2 + j]

        out = Tensor(out_flat, (self, other), 'matmul')
        out.shape = (r1, c2)

        def _backward():
            for i in range(r1):
                for k in range(c1):
                    for j in range(c2):
                        g = out.grad[i * c2 + j]
                        self.grad[i * c1 + k] += other.data[k * c2 + j] * g
                        other.grad[k * c2 + j] += self.data[i * c1 + k] * g
        out._backward = _backward
        return out

    def relu(self) -> 'Tensor':
        out_data = [max(0.0, x) for x in self.data]
        out = Tensor(out_data, (self,), 'ReLU')
        out.shape = self.shape

        def _backward():
            for i in range(len(self.data)):
                self.grad[i] += (1.0 if self.data[i] > 0.0 else 0.0) * out.grad[i]
        out._backward = _backward
        return out

    def tanh(self) -> 'Tensor':
        out_data = [math.tanh(x) for x in self.data]
        out = Tensor(out_data, (self,), 'tanh')
        out.shape = self.shape

        def _backward():
            for i in range(len(self.data)):
                t = out.data[i]
                self.grad[i] += (1.0 - t * t) * out.grad[i]
        out._backward = _backward
        return out

    def sum(self) -> 'Tensor':
        out_val = sum(self.data)
        out = Tensor([out_val], (self,), 'sum')
        out.shape = (1,)

        def _backward():
            for i in range(len(self.data)):
                self.grad[i] += 1.0 * out.grad[0]
        out._backward = _backward
        return out

    def backward(self):
        topo: List['Tensor'] = []
        visited: Set['Tensor'] = set()

        def build_topo(v: 'Tensor'):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)
        self.grad = [1.0] * len(self.data)
        for node in reversed(topo):
            node._backward()

class Linear:
    def __init__(self, in_features: int, out_features: int):
        scale = math.sqrt(2.0 / in_features)
        weights_data = [[random.gauss(0.0, scale) for _ in range(out_features)] for _ in range(in_features)]
        self.W = Tensor(weights_data)
        self.b = Tensor([[0.0] * out_features])

    def __call__(self, x: Tensor) -> Tensor:
        out = x.matmul(self.W)
        r, c = out.shape
        repeated_b_data = self.b.data * r
        bias_tensor = Tensor(repeated_b_data)
        bias_tensor.shape = (r, c)
        return out + bias_tensor

    def parameters(self) -> List[Tensor]:
        return [self.W, self.b]

class SGDOptimizer:
    def __init__(self, params: List[Tensor], lr: float = 0.01):
        self.params = params
        self.lr = lr

    def step(self):
        for p in self.params:
            for i in range(len(p.data)):
                p.data[i] -= self.lr * p.grad[i]

    def zero_grad(self):
        for p in self.params:
            p.zero_grad()
