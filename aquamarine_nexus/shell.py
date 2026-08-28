import readline
import ast
from aquamarine_nexus.registry import get_full_registry
from aquamarine_nexus.validator import AutoValidator

class NexusInteractiveShell:
    """Scientific REPL with Variable Scoping & Pipeline Chaining"""

    @classmethod
    def start(cls):
        registry = get_full_registry()
        session_vars = {}

        # Autocompletion
        def completer(text, state):
            options = [cmd for cmd in registry.keys() if cmd.startswith(text)]
            return options[state] if state < len(options) else None

        readline.set_completer(completer)
        readline.parse_and_bind("tab: complete")

        print("\n" + "="*70)
        print("  💠 AQUAMARINE NEXUS INTERACTIVE SCIENTIFIC SHELL")
        print("  Type 'list', 'docs', 'test', 'exit' or '<var> = <engine> <args>'")
        print("="*70 + "\n")

        while True:
            try:
                line = input("nexus> ").strip()
                if not line:
                    continue
                if line.lower() in ("exit", "quit"):
                    break
                if line.lower() == "list":
                    for k in sorted(registry.keys()):
                        print(f" • {k}")
                    continue

                # Variable assignment parsing: x = engine args...
                target_var = None
                if "=" in line and not line.startswith("="):
                    parts = line.split("=", 1)
                    target_var = parts[0].strip()
                    line = parts[1].strip()

                tokens = line.split()
                engine = tokens[0]
                args = tokens[1:]

                # Resolve session variables in arguments
                resolved_args = []
                for a in args:
                    if a in session_vars:
                        resolved_args.append(str(session_vars[a]))
                    else:
                        resolved_args.append(a)

                if engine not in registry:
                    print(f"[!] Unknown engine '{engine}'.")
                    continue

                func = registry[engine]
                result = AutoValidator.execute_with_validation(func, resolved_args)

                if result is not None:
                    if target_var:
                        session_vars[target_var] = result
                        print(f"[{target_var}] <=")
                    if isinstance(result, dict):
                        for k, v in result.items():
                            print(f" • {k}: {v}")
                    else:
                        print(f" • Result: {result}")

            except (KeyboardInterrupt, EOFError):
                print("\nExiting shell.")
                break
            except Exception as e:
                print(f"[!] Error: {e}")
