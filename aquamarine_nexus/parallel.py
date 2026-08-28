from concurrent.futures import ProcessPoolExecutor
from aquamarine_nexus.registry import get_full_registry
from aquamarine_nexus.validator import AutoValidator

class ParallelBatchRunner:
    """Multiprocessing Batch Execution Core for Large Parametric Sweeps"""

    @staticmethod
    def _worker(task):
        engine_name, args = task
        registry = get_full_registry()
        func = registry[engine_name]
        return AutoValidator.execute_with_validation(func, args)

    @classmethod
    def run_batch(cls, engine_name: str, batch_args: list, max_workers: int = None):
        tasks = [(engine_name, args) for args in batch_args]
        print(f"\n[*] Launching parallel sweep: {len(tasks)} tasks across CPU cores...")

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(cls._worker, tasks))

        print(f"[+] Successfully executed {len(results)} tasks in parallel.\n")
        return results
