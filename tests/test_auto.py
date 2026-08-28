# Auto-generated Nexus Test Suite
import pytest
from aquamarine_nexus.registry import get_full_registry

REGISTRY = get_full_registry()

@pytest.mark.parametrize('engine_name', list(REGISTRY.keys()))
def test_engine_callable(engine_name):
    func = REGISTRY[engine_name]
    assert callable(func), f'Engine {engine_name} is not callable'
