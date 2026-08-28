import math

class Expr:
    """Base Abstract Node for all Symbolic Expressions."""
    def diff(self, var: 'Symbol') -> 'Expr':
        raise NotImplementedError

    def eval(self, env: dict) -> float:
        raise NotImplementedError

    def simplify(self) -> 'Expr':
        return self

    def __add__(self, other): return Add(self, _to_expr(other))
    def __radd__(self, other): return Add(_to_expr(other), self)
    def __sub__(self, other): return Sub(self, _to_expr(other))
    def __rsub__(self, other): return Sub(_to_expr(other), self)
    def __mul__(self, other): return Mul(self, _to_expr(other))
    def __rmul__(self, other): return Mul(_to_expr(other), self)
    def __pow__(self, power): return Pow(self, _to_expr(power))
    def __rpow__(self, base): return Pow(_to_expr(base), self)
    def __truediv__(self, other): return Div(self, _to_expr(other))
    def __rtruediv__(self, other): return Div(_to_expr(other), self)
    def __neg__(self): return Mul(Const(-1.0), self)

def _to_expr(x):
    return x if isinstance(x, Expr) else Const(x)

def _simplify(expr):
    if hasattr(expr, 'simplify'):
        return expr.simplify()
    return expr

class Symbol(Expr):
    def __init__(self, name: str):
        self.name = str(name)

    def diff(self, var: 'Symbol') -> Expr:
        return Const(1.0) if self.name == var.name else Const(0.0)

    def eval(self, env: dict) -> float:
        if self.name not in env:
            raise KeyError(f"Variable '{self.name}' not bound.")
        return float(env[self.name])

    def __repr__(self):
        return self.name

class Const(Expr):
    def __init__(self, value: float):
        self.value = float(value)

    def diff(self, var: Symbol) -> Expr:
        return Const(0.0)

    def eval(self, env: dict) -> float:
        return self.value

    def __repr__(self):
        return f"{self.value:g}"

class Add(Expr):
    def __init__(self, left, right):
        self.left = _to_expr(left)
        self.right = _to_expr(right)

    def diff(self, var: Symbol) -> Expr:
        return Add(self.left.diff(var), self.right.diff(var)).simplify()

    def eval(self, env: dict) -> float:
        return self.left.eval(env) + self.right.eval(env)

    def simplify(self) -> Expr:
        l, r = _simplify(self.left), _simplify(self.right)
        if isinstance(l, Const) and isinstance(r, Const): return Const(l.value + r.value)
        if isinstance(l, Const) and l.value == 0: return r
        if isinstance(r, Const) and r.value == 0: return l
        return Add(l, r)

    def __repr__(self): return f"({self.left} + {self.right})"

class Sub(Expr):
    def __init__(self, left, right):
        self.left = _to_expr(left)
        self.right = _to_expr(right)

    def diff(self, var: Symbol) -> Expr:
        return Sub(self.left.diff(var), self.right.diff(var)).simplify()

    def eval(self, env: dict) -> float:
        return self.left.eval(env) - self.right.eval(env)

    def simplify(self) -> Expr:
        l, r = _simplify(self.left), _simplify(self.right)
        if isinstance(l, Const) and isinstance(r, Const): return Const(l.value - r.value)
        if isinstance(r, Const) and r.value == 0: return l
        return Sub(l, r)

    def __repr__(self): return f"({self.left} - {self.right})"

class Mul(Expr):
    def __init__(self, left, right):
        self.left = _to_expr(left)
        self.right = _to_expr(right)

    def diff(self, var: Symbol) -> Expr:
        return Add(Mul(self.left.diff(var), self.right), Mul(self.left, self.right.diff(var))).simplify()

    def eval(self, env: dict) -> float:
        return self.left.eval(env) * self.right.eval(env)

    def simplify(self) -> Expr:
        l, r = _simplify(self.left), _simplify(self.right)
        if isinstance(l, Const) and isinstance(r, Const): return Const(l.value * r.value)
        if (isinstance(l, Const) and l.value == 0) or (isinstance(r, Const) and r.value == 0): return Const(0.0)
        if isinstance(l, Const) and l.value == 1: return r
        if isinstance(r, Const) and r.value == 1: return l
        return Mul(l, r)

    def __repr__(self): return f"({self.left} * {self.right})"

class Div(Expr):
    def __init__(self, left, right):
        self.left = _to_expr(left)
        self.right = _to_expr(right)

    def diff(self, var: Symbol) -> Expr:
        num = Sub(Mul(self.left.diff(var), self.right), Mul(self.left, self.right.diff(var)))
        den = Pow(self.right, Const(2.0))
        return Div(num, den).simplify()

    def eval(self, env: dict) -> float:
        d = self.right.eval(env)
        if d == 0: raise ZeroDivisionError("Division by zero.")
        return self.left.eval(env) / d

    def simplify(self) -> Expr:
        l, r = _simplify(self.left), _simplify(self.right)
        if isinstance(l, Const) and isinstance(r, Const): return Const(l.value / r.value)
        if isinstance(l, Const) and l.value == 0: return Const(0.0)
        if isinstance(r, Const) and r.value == 1: return l
        return Div(l, r)

    def __repr__(self): return f"({self.left} / {self.right})"

class Pow(Expr):
    def __init__(self, base, exp):
        self.base = _to_expr(base)
        self.exp = _to_expr(exp)

    def diff(self, var: Symbol) -> Expr:
        if isinstance(self.exp, Const):
            n = self.exp.value
            return Mul(Mul(Const(n), Pow(self.base, Const(n - 1.0))), self.base.diff(var)).simplify()
        raise NotImplementedError("Variable exponents require generalized derivative.")

    def eval(self, env: dict) -> float:
        return self.base.eval(env) ** self.exp.eval(env)

    def simplify(self) -> Expr:
        b, e = _simplify(self.base), _simplify(self.exp)
        if isinstance(e, Const) and e.value == 0: return Const(1.0)
        if isinstance(e, Const) and e.value == 1: return b
        if isinstance(b, Const) and isinstance(e, Const): return Const(b.value ** e.value)
        return Pow(b, e)

    def __repr__(self): return f"({self.base}^{self.exp})"

class Sin(Expr):
    def __init__(self, arg): self.arg = _to_expr(arg)
    def diff(self, var: Symbol) -> Expr: return Mul(Cos(self.arg), self.arg.diff(var)).simplify()
    def eval(self, env: dict) -> float: return math.sin(self.arg.eval(env))
    def simplify(self) -> Expr: return Sin(_simplify(self.arg))
    def __repr__(self): return f"sin({self.arg})"

class Cos(Expr):
    def __init__(self, arg): self.arg = _to_expr(arg)
    def diff(self, var: Symbol) -> Expr: return Mul(Mul(Const(-1.0), Sin(self.arg)), self.arg.diff(var)).simplify()
    def eval(self, env: dict) -> float: return math.cos(self.arg.eval(env))
    def simplify(self) -> Expr: return Cos(_simplify(self.arg))
    def __repr__(self): return f"cos({self.arg})"

class Exp(Expr):
    def __init__(self, arg): self.arg = _to_expr(arg)
    def diff(self, var: Symbol) -> Expr: return Mul(Exp(self.arg), self.arg.diff(var)).simplify()
    def eval(self, env: dict) -> float: return math.exp(self.arg.eval(env))
    def simplify(self) -> Expr: return Exp(_simplify(self.arg))
    def __repr__(self): return f"exp({self.arg})"

class Ln(Expr):
    def __init__(self, arg): self.arg = _to_expr(arg)
    def diff(self, var: Symbol) -> Expr: return Div(self.arg.diff(var), self.arg).simplify()
    def eval(self, env: dict) -> float: return math.log(self.arg.eval(env))
    def simplify(self) -> Expr: return Ln(_simplify(self.arg))
    def __repr__(self): return f"ln({self.arg})"
