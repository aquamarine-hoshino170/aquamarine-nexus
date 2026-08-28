import math
from aquamarine_nexus.core.sovereign_formula_registry import FormulaRegistry

print("=" * 75)
print("  ❖ INFINITY FORMULA ENGINE - STRESS & PRECISION BENCHMARK ❖")
print("=" * 75)

# ----------------------------------------------------------------------
# Test 1: Swish Activation Formula -> f(x) = x * sigmoid(beta * x)
# Analytical Gradient dy/dx = beta*f(x) + sigmoid(beta*x)*(1 - beta*f(x))
# ----------------------------------------------------------------------
def swish_op(inputs):
    x = inputs[0]
    beta = inputs[1] if len(inputs) > 1 else 1.0
    sig = 1.0 / (1.0 + math.exp(-max(min(beta * x, 20.0), -20.0)))
    return [x * sig]

FormulaRegistry.register('swish', forward_fn=swish_op)
x_in = 1.5
swish_out = FormulaRegistry.execute('swish', [x_in, 1.0])[0]
swish_grad = FormulaRegistry.backprop('swish', [x_in, 1.0], grad_output=[1.0])[0]

# Theoretical Target Calculation
sig_val = 1.0 / (1.0 + math.exp(-x_in))
expected_swish = x_in * sig_val
expected_grad = sig_val + x_in * sig_val * (1.0 - sig_val)

print(f"\n[Test 1: Non-linear Activation (Swish)]")
print(f"  Input x           : {x_in}")
print(f"  Computed Output   : {swish_out:.6f} (Expected: {expected_swish:.6f})")
print(f"  Autograd dy/dx    : {swish_grad:.6f} (Expected: {expected_grad:.6f})")
err_swish = abs(swish_out - expected_swish) + abs(swish_grad - expected_grad)
print(f"  Status            : {'✓ PASSED (Error < 1e-4)' if err_swish < 1e-4 else '✗ FAILED'}")

# ----------------------------------------------------------------------
# Test 2: Relativistic Energy-Momentum Relation -> E = sqrt( (p*c)^2 + (m0*c^2)^2 )
# c = 3.0 (normalized), p = 4.0, m0 = 1.0
# ----------------------------------------------------------------------
def relativistic_energy_op(inputs):
    p, m0, c = inputs[0], inputs[1], inputs[2]
    return [math.sqrt((p * c)**2 + (m0 * c**2)**2)]

FormulaRegistry.register('relativistic_energy', forward_fn=relativistic_energy_op)
p_val, m0_val, c_val = 4.0, 1.0, 3.0
e_out = FormulaRegistry.execute('relativistic_energy', [p_val, m0_val, c_val])[0]
# p*c = 12, m0*c^2 = 9 => sqrt(144 + 81) = sqrt(225) = 15.0
expected_e = 15.0

print(f"\n[Test 2: Quantum/Relativistic Invariant (E^2 = p^2*c^2 + m0^2*c^4)]")
print(f"  Inputs (p, m0, c) : ({p_val}, {m0_val}, {c_val})")
print(f"  Computed Energy E : {e_out:.6f} (Expected: {expected_e:.6f})")
err_e = abs(e_out - expected_e)
print(f"  Status            : {'✓ PASSED (Exact Invariant)' if err_e < 1e-7 else '✗ FAILED'}")

# ----------------------------------------------------------------------
# Test 3: Shannon Information Entropy -> H(X) = - sum(p_i * log2(p_i))
# For fair 4-state system [0.25, 0.25, 0.25, 0.25] -> H(X) = 2.0 bits
# ----------------------------------------------------------------------
def shannon_entropy_op(inputs):
    h = 0.0
    for p in inputs:
        if p > 0.0:
            h -= p * math.log2(p)
    return [h]

FormulaRegistry.register('shannon_entropy', forward_fn=shannon_entropy_op)
probs = [0.25, 0.25, 0.25, 0.25]
entropy_out = FormulaRegistry.execute('shannon_entropy', probs)[0]
expected_entropy = 2.0

print(f"\n[Test 3: Information Theory (Shannon Entropy)]")
print(f"  Probability Vector: {probs}")
print(f"  Computed Entropy  : {entropy_out:.6f} bits (Expected: {expected_entropy:.6f} bits)")
err_h = abs(entropy_out - expected_entropy)
print(f"  Status            : {'✓ PASSED' if err_h < 1e-7 else '✗ FAILED'}")

# ----------------------------------------------------------------------
# Test 4: Extreme Numerical Stability (Underflow / Overflow Test)
# Numerically unstable Softplus: log(1 + exp(x)) for x = 1000.0 (Must not overflow to Inf)
# ----------------------------------------------------------------------
def stable_softplus_op(inputs):
    x = inputs[0]
    # For large x, log(1 + e^x) ~ x
    if x > 30.0:
        return [x]
    elif x < -30.0:
        return [math.exp(x)]
    return [math.log1p(math.exp(x))]

FormulaRegistry.register('stable_softplus', forward_fn=stable_softplus_op)
extreme_x = 1000.0
softplus_out = FormulaRegistry.execute('stable_softplus', [extreme_x])[0]

print(f"\n[Test 4: Numerical Boundary & Float Stability]")
print(f"  Extreme Input x   : {extreme_x}")
print(f"  Computed Output   : {softplus_out:.6f} (Expected: 1000.000000)")
err_stab = abs(softplus_out - extreme_x)
print(f"  Status            : {'✓ PASSED (Zero Overflow)' if err_stab < 1e-7 else '✗ FAILED'}")
print("=" * 75)
