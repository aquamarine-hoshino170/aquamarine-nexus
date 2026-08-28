import argparse
import sys
import math
from aquamarine_nexus.io_core import NexusIO
from aquamarine_nexus.registry import get_full_registry
from aquamarine_nexus.validator import AutoValidator
from aquamarine_nexus.auto_docs import AutoDocAndTestGenerator
from aquamarine_nexus.shell import NexusInteractiveShell

MODULE_REGISTRY = get_full_registry()

def main():
    parser = argparse.ArgumentParser(prog="aquamarine-nexus", description="Aquamarine Nexus Universal Scientific Framework")
    parser.add_argument("--list", action="store_true", help="List all available engines")
    parser.add_argument("--shell", action="store_true", help="Launch interactive scientific REPL shell")
    parser.add_argument("--gen-docs", action="store_true", help="Auto-generate DOCS.md & tests/test_auto.py")
    parser.add_argument("--run", nargs="+", metavar=("ENGINE", "PARAMS..."), help="Execute any engine with custom parameters")
    parser.add_argument("--export-json", metavar="FILEPATH", help="Export result to JSON")
    parser.add_argument("--export-csv", metavar="FILEPATH", help="Export matrix result to CSV")

    args = parser.parse_args()

    if args.shell:
        NexusInteractiveShell.start()
        return

    if args.gen-docs if hasattr(args, 'gen-docs') else False or (len(sys.argv) > 1 and sys.argv[1] == "--gen-docs"):
        AutoDocAndTestGenerator.generate_markdown_docs()
        AutoDocAndTestGenerator.generate_automated_tests()
        return

    if args.list:
        print("\n" + "="*80)
        print("   AQUAMARINE NEXUS - FULL DYNAMIC ENGINE REGISTRY")
        print("="*80)
        for name, func in sorted(MODULE_REGISTRY.items()):
            doc = func.__doc__.strip().split('\n')[0] if func.__doc__ else "No description"
            print(f" • {name:<25} -> {doc}")
        print("="*80 + "\n")
        return

    if args.run:
        engine_name = args.run[0]
        raw_inputs = args.run[1:]

        if engine_name not in MODULE_REGISTRY:
            print(f"\n[ERROR] Unknown engine '{engine_name}'. Run '--list' for all options.\n")
            return

        target_func = MODULE_REGISTRY[engine_name]
        try:
            result = AutoValidator.execute_with_validation(target_func, raw_inputs)
            if result is None:
                return

            print(f"\n[SUCCESSFUL EXECUTION: {engine_name}]")
            if isinstance(result, dict):
                for k, v in result.items():
                    print(f" • {k}: {v}")
            elif isinstance(result, list):
                for item in result[:10]:
                    print(f" • {item}")
                if len(result) > 10:
                    print(f" ... [{len(result)-10} more items] ...")
            else:
                print(f" • Output Result: {result}")

            if args.export_json:
                res_dict = result if isinstance(result, dict) else {"output": result}
                exp_status = NexusIO.export_json(res_dict, args.export_json)
                print(f" [Exported to JSON -> {exp_status['filepath']}]")

            if args.export_csv:
                res_matrix = result if isinstance(result, list) else [[result]]
                exp_status = NexusIO.export_csv(res_matrix, args.export_csv)
                print(f" [Exported to CSV -> {exp_status['filepath']}]")

            print()
        except Exception as e:
            print(f"\n[RUNTIME EXECUTION ERROR in {engine_name}]: {e}\n")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
