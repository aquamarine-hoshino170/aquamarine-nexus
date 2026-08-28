__version__ = "2.4.0"

import inspect
import importlib
import pkgutil

# Direct I/O Shortcuts
from .io_core import NexusIO
export_json = NexusIO.export_json
import_json = NexusIO.import_json
export_csv = NexusIO.export_csv
import_csv = NexusIO.import_csv
export_serialized = NexusIO.export_serialized
import_serialized = NexusIO.import_serialized

# Dynamically export all classes across submodules
__all__ = ["NexusIO", "export_json", "import_json", "export_csv", "import_csv", "export_serialized", "import_serialized"]

for _, _modname, _ in pkgutil.walk_packages(__path__, __name__ + "."):
    if _modname.endswith(".registry") or _modname.endswith(".cli"):
        continue
    try:
        _mod = importlib.import_module(_modname)
        for _name, _obj in inspect.getmembers(_mod, inspect.isclass):
            if _obj.__module__.startswith("aquamarine_nexus"):
                globals()[_name] = _obj
                if _name not in __all__:
                    __all__.append(_name)
    except Exception:
        pass
