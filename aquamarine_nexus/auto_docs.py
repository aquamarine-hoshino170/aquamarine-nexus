import os
import inspect
from aquamarine_nexus.registry import get_full_registry

class AutoDocAndTestGenerator:
    """Self-Documenting LaTeX Generator & Test Suite Synthesizer"""

    @staticmethod
    def generate_markdown_docs(output_path="DOCS.md"):
        registry = get_full_registry()
        lines = [
            "# 🌌 Aquamarine Nexus — Complete Scientific Catalog",
            "",
            "> Auto-generated ecosystem reference and mathematical registry.",
            "",
            "| Command / Engine | Type Signature | Scientific Description |",
            "| :--- | :--- | :--- |"
        ]

        for name, func in sorted(registry.items()):
            try:
                sig = str(inspect.signature(func))
            except Exception:
                sig = "(*args)"
            doc = func.__doc__.strip().split('\n')[0] if func.__doc__ else "Core numerical routine"
            doc_clean = doc.replace("|", "\\|")
            lines.append(f"| `{name}` | `{sig}` | {doc_clean} |")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"[+] Documentation generated -> {output_path}")

    @staticmethod
    def generate_automated_tests(output_path="tests/test_auto.py"):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        registry = get_full_registry()

        code = [
            "# Auto-generated Nexus Test Suite",
            "import pytest",
            "from aquamarine_nexus.registry import get_full_registry",
            "",
            "REGISTRY = get_full_registry()",
            "",
            "@pytest.mark.parametrize('engine_name', list(REGISTRY.keys()))",
            "def test_engine_callable(engine_name):",
            "    func = REGISTRY[engine_name]",
            "    assert callable(func), f'Engine {engine_name} is not callable'"
        ]

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(code) + "\n")
        print(f"[+] Automated test suite generated -> {output_path}")
