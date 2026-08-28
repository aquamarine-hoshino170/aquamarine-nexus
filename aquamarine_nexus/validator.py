import inspect
import ast
import typing
from aquamarine_nexus.units import UnitConverter

class AutoValidator:
    """Intelligent Type Inference, SI Unit Parsing & Signature Validation"""

    @staticmethod
    def parse_value_with_type(val_str: str, expected_type):
        # 1. Automatic Unit Parsing Check
        unit_val = UnitConverter.parse_quantity(val_str)
        if unit_val is not None:
            return unit_val

        # 2. General type inference
        if expected_type == inspect.Parameter.empty or expected_type == typing.Any:
            try:
                return ast.literal_eval(val_str)
            except Exception:
                try:
                    if "." in val_str or "e" in val_str.lower():
                        return float(val_str)
                    return int(val_str)
                except ValueError:
                    return val_str

        if expected_type == bool:
            return val_str.lower() in ("true", "1", "yes", "t")
        if expected_type in (int, float, str):
            return expected_type(val_str)
        if expected_type in (list, dict, tuple, set):
            return ast.literal_eval(val_str)

        try:
            return ast.literal_eval(val_str)
        except Exception:
            return expected_type(val_str)

    @classmethod
    def execute_with_validation(cls, func, raw_args: list):
        sig = inspect.signature(func)
        params = list(sig.parameters.values())

        required_params = [p for p in params if p.default == inspect.Parameter.empty]
        total_params = params

        if len(raw_args) < len(required_params):
            print("\n" + "="*70)
            print(f" [!] PARAMETER MISMATCH FOR ENGINE: '{func.__name__}'")
            print("="*70)
            print(f" • Expected Signature: {func.__name__}{sig}")
            print(f" • Required Arguments ({len(required_params)}):")
            for p in required_params:
                t_name = p.annotation.__name__ if p.annotation != inspect.Parameter.empty else "Any"
                print(f"    - {p.name:<22} [Type: {t_name}]")
            print("="*70 + "\n")
            return None

        casted_args = []
        for i, val in enumerate(raw_args):
            if i < len(total_params):
                param = total_params[i]
                try:
                    casted = cls.parse_value_with_type(str(val), param.annotation)
                    casted_args.append(casted)
                except Exception as e:
                    print(f"\n[TYPE CAST ERROR] Parameter '{param.name}': {e}\n")
                    return None
            else:
                try:
                    casted_args.append(ast.literal_eval(str(val)))
                except Exception:
                    casted_args.append(val)

        return func(*casted_args)
