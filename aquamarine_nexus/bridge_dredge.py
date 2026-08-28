try:
    from dredge.omni_kernel import OmniVerseCore
except ImportError:
    OmniVerseCore = None

class DredgeBridge:
    """Seamless Interface to all 340 Equations of aquamarine-dredge"""

    @staticmethod
    def call_dredge_engine(engine_name: str, *params):
        if OmniVerseCore is None:
            raise ImportError("aquamarine-dredge is not installed in the environment.")
        if not hasattr(OmniVerseCore, engine_name):
            raise AttributeError(f"Engine '{engine_name}' does not exist in aquamarine-dredge.")
        func = getattr(OmniVerseCore, engine_name)
        return func(*params) if params else func()
