import os
import sys
import inspect
import importlib.util

def get_full_registry():
    from aquamarine_nexus.io_core import NexusIO
    registry = {
        "import_json": NexusIO.import_json,
        "import_csv": NexusIO.import_csv,
    }

    base_dir = os.path.dirname(os.path.abspath(__file__))

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("__") and file not in ("registry.py", "cli.py"):
                file_path = os.path.join(root, file)
                mod_name = file[:-3]
                
                try:
                    spec = importlib.util.spec_from_file_location(mod_name, file_path)
                    if spec and spec.loader:
                        mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(mod)

                        for _, cls_obj in inspect.getmembers(mod, inspect.isclass):
                            if cls_obj.__module__ == mod_name:
                                for m_name, func in inspect.getmembers(cls_obj, predicate=inspect.isfunction):
                                    if not m_name.startswith("_"):
                                        registry[m_name] = func
                                        
                                        parts = m_name.split("_")
                                        if len(parts) > 1:
                                            short_name = "_".join(parts[-2:])
                                            if short_name not in registry:
                                                registry[short_name] = func
                except Exception as e:
                    print(f"[REGISTRY LOAD WARNING] Error loading {file}: {e}")

    try:
        from aquamarine_nexus.bridge_dredge import DredgeBridge
        registry["dredge"] = DredgeBridge.call_dredge_engine
    except Exception:
        pass

    return registry
