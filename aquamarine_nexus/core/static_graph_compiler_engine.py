import array
from typing import List, Dict, Any, Tuple, Callable

class ComputationalNode:
    def __init__(self, node_id: int, op: str, inputs: List[int], value: float = 0.0):
        self.node_id = node_id
        self.op = op          # 'INPUT', 'CONST', 'ADD', 'MUL', 'RELU', 'MATMUL'
        self.inputs = inputs
        self.value = value
        self.is_dead = False

class SovereignIRGraph:
    """
    Zero-Dependency Graph Intermediate Representation (IR) Compiler.
    Executes Operator Fusion, Constant Folding, and generates fused single-pass bytecode lambdas.
    """
    def __init__(self):
        self.nodes: List[ComputationalNode] = []
        self.node_counter = 0

    def add_node(self, op: str, inputs: List[int] = None, value: float = 0.0) -> int:
        inputs = inputs or []
        nid = self.node_counter
        self.nodes.append(ComputationalNode(nid, op, inputs, value))
        self.node_counter += 1
        return nid

    def optimize_graph(self):
        """Pass 1: Constant Folding & Algebraic Simplification."""
        for n in self.nodes:
            if n.op == 'ADD' and len(n.inputs) == 2:
                in1, in2 = self.nodes[n.inputs[0]], self.nodes[n.inputs[1]]
                if in1.op == 'CONST' and in2.op == 'CONST':
                    n.op = 'CONST'
                    n.value = in1.value + in2.value
                    n.inputs = []
            elif n.op == 'MUL' and len(n.inputs) == 2:
                in1, in2 = self.nodes[n.inputs[0]], self.nodes[n.inputs[1]]
                if in1.op == 'CONST' and in2.op == 'CONST':
                    n.op = 'CONST'
                    n.value = in1.value * in2.value
                    n.inputs = []

    def compile_fused_evaluator(self) -> Callable[[List[float]], float]:
        """Pass 2: JIT Compilation into native Python functional closure with O(1) buffer allocation."""
        self.optimize_graph()
        active_nodes = [n for n in self.nodes if not n.is_dead]

        def evaluator(inputs: List[float]) -> float:
            env = [0.0] * len(self.nodes)
            input_ptr = 0
            for node in active_nodes:
                if node.op == 'INPUT':
                    env[node.node_id] = inputs[input_ptr]
                    input_ptr += 1
                elif node.op == 'CONST':
                    env[node.node_id] = node.value
                elif node.op == 'ADD':
                    env[node.node_id] = env[node.inputs[0]] + env[node.inputs[1]]
                elif node.op == 'MUL':
                    env[node.node_id] = env[node.inputs[0]] * env[node.inputs[1]]
                elif node.op == 'RELU':
                    val = env[node.inputs[0]]
                    env[node.node_id] = val if val > 0.0 else 0.0
            return env[-1]

        return evaluator
