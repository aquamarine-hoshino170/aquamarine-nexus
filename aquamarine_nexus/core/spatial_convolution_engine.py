import math
import random
from typing import List, Tuple
from aquamarine_nexus.core.sovereign_tensor_engine import Tensor

class Conv2D:
    """
    Pure-Python 2D Spatial Convolution Layer.
    Input shape: (C_in, H_in, W_in) -> Output shape: (C_out, H_out, W_out)
    """
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 3, stride: int = 1):
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.stride = stride

        scale = math.sqrt(2.0 / (in_channels * kernel_size * kernel_size))
        weight_data = [
            [[[random.gauss(0.0, scale) for _ in range(kernel_size)] for _ in range(kernel_size)]
             for _ in range(in_channels)]
            for _ in range(out_channels)
        ]
        self.W = Tensor(weight_data)
        self.b = Tensor([0.0] * out_channels)

    def forward_spatial(self, x: Tensor, c_in: int, h_in: int, w_in: int) -> Tuple[Tensor, int, int, int]:
        k = self.kernel_size
        s = self.stride
        h_out = (h_in - k) // s + 1
        w_out = (w_in - k) // s + 1

        out_data = [0.0] * (self.out_channels * h_out * w_out)

        for oc in range(self.out_channels):
            b_val = self.b.data[oc]
            for oh in range(h_out):
                for ow in range(w_out):
                    ih_start = oh * s
                    iw_start = ow * s
                    acc = b_val
                    for ic in range(c_in):
                        for kh in range(k):
                            for kw in range(k):
                                x_idx = ic * (h_in * w_in) + (ih_start + kh) * w_in + (iw_start + kw)
                                w_idx = oc * (c_in * k * k) + ic * (k * k) + kh * k + kw
                                acc += x.data[x_idx] * self.W.data[w_idx]
                    out_data[oc * (h_out * w_out) + oh * w_out + ow] = acc

        out = Tensor(out_data, (x, self.W, self.b), 'conv2d')
        out.shape = (self.out_channels, h_out, w_out)

        def _backward():
            for oc in range(self.out_channels):
                for oh in range(h_out):
                    for ow in range(w_out):
                        g = out.grad[oc * (h_out * w_out) + oh * w_out + ow]
                        self.b.grad[oc] += g
                        ih_start = oh * s
                        iw_start = ow * s
                        for ic in range(c_in):
                            for kh in range(k):
                                for kw in range(k):
                                    x_idx = ic * (h_in * w_in) + (ih_start + kh) * w_in + (iw_start + kw)
                                    w_idx = oc * (c_in * k * k) + ic * (k * k) + kh * k + kw
                                    x.grad[x_idx] += self.W.data[w_idx] * g
                                    self.W.grad[w_idx] += x.data[x_idx] * g
        out._backward = _backward
        return out, self.out_channels, h_out, w_out

    def parameters(self) -> List[Tensor]:
        return [self.W, self.b]

class MaxPool2D:
    """
    Pure-Python 2D Spatial Max-Pooling Layer.
    """
    def __init__(self, kernel_size: int = 2, stride: int = 2):
        self.kernel_size = kernel_size
        self.stride = stride

    def forward_spatial(self, x: Tensor, c_in: int, h_in: int, w_in: int) -> Tuple[Tensor, int, int, int]:
        k = self.kernel_size
        s = self.stride
        h_out = (h_in - k) // s + 1
        w_out = (w_in - k) // s + 1

        out_data = [0.0] * (c_in * h_out * w_out)
        max_indices = [0] * (c_in * h_out * w_out)

        for c in range(c_in):
            for oh in range(h_out):
                for ow in range(w_out):
                    ih_start = oh * s
                    iw_start = ow * s
                    max_val = -float('inf')
                    best_idx = 0
                    for kh in range(k):
                        for kw in range(k):
                            idx = c * (h_in * w_in) + (ih_start + kh) * w_in + (iw_start + kw)
                            val = x.data[idx]
                            if val > max_val:
                                max_val = val
                                best_idx = idx
                    out_idx = c * (h_out * w_out) + oh * w_out + ow
                    out_data[out_idx] = max_val
                    max_indices[out_idx] = best_idx

        out = Tensor(out_data, (x,), 'maxpool2d')
        out.shape = (c_in, h_out, w_out)

        def _backward():
            for i, target_idx in enumerate(max_indices):
                x.grad[target_idx] += out.grad[i]
        out._backward = _backward
        return out, c_in, h_out, w_out
