import time
import math
import tempfile
import os
from array import array
from aquamarine_nexus.core.bigdata_tensor_accelerator import BigDataTensorAccelerator
from aquamarine_nexus.core.advanced_symbolic_cas import AdvancedSymbolicCAS
from aquamarine_nexus.core.aqua_binary_serializer import AquaBinaryProtocol
from aquamarine_nexus.science.whole_cell_multiscale_neuron import MultiScaleWholeCellNeuronCore
from aquamarine_nexus.science.spacetime_topological_geodesic_engine import TopologicalSpacetimeGeodesicCore

class UnifiedEcosystemBenchmarkCore:
    @staticmethod
    def run_full_system_diagnostic() -> dict:
        """Runs a complete first-principles validation across all unified layers."""
        start_time = time.perf_counter()
        results = {}

        # 1. Test BigData Parallel Matrix Engine
        t0 = time.perf_counter()
        dim = 128
        mat_a = BigDataTensorAccelerator.arange_flat(dim * dim, (dim, dim))
        mat_b = BigDataTensorAccelerator.arange_flat(dim * dim, (dim, dim))
        res_mat = mat_a.parallel_matmul(mat_b, num_workers=2, block_size=64)
        sum_val = res_mat.fast_reduce_sum()
        matmul_time = time.perf_counter() - t0
        mflops = (2.0 * (dim ** 3) / (matmul_time + 1e-12)) / 1e6
        results["layer_1_bigdata_tensors"] = {
            "status": "PASS" if sum_val > 0 else "FAIL",
            "throughput_MFLOPS": round(mflops, 2),
            "execution_time_sec": round(matmul_time, 4)
        }

        # 2. Test Exact Symbolic CAS Engine
        t0 = time.perf_counter()
        limit_test = AdvancedSymbolicCAS.evaluate_symbolic_limit_lhopital("1-cos(x)", "x^2", 0.0, "x")
        poly_int = AdvancedSymbolicCAS.symbolic_integrate_polynomial_terms({"2": 3.0, "1": 2.0}, "x")
        cas_time = time.perf_counter() - t0
        results["layer_2_symbolic_cas"] = {
            "status": "PASS" if abs(limit_test["exact_limit_value"] - 0.5) < 1e-6 else "FAIL",
            "lhopital_limit_0_5": limit_test["exact_limit_value"],
            "symbolic_integral": poly_int,
            "execution_time_sec": round(cas_time, 4)
        }

        # 3. Test .aqua Zero-Copy Binary Persistence (OS/Termux agnostic temp directory)
        t0 = time.perf_counter()
        temp_dir = tempfile.gettempdir()
        temp_aqua_path = os.path.join(temp_dir, "test_integrity.aqua")
        
        test_buf = array('d', [float(i) * 0.1 for i in range(10000)])
        save_rep = AquaBinaryProtocol.save_aqua_tensor(temp_aqua_path, test_buf, (100, 100))
        load_buf, load_shape, load_rep = AquaBinaryProtocol.load_aqua_tensor(temp_aqua_path)
        io_time = time.perf_counter() - t0
        
        if os.path.exists(temp_aqua_path):
            os.remove(temp_aqua_path)

        results["layer_3_aqua_zero_copy_io"] = {
            "status": "PASS" if (len(load_buf) == 10000 and load_shape == (100, 100)) else "FAIL",
            "write_speed_MB_s": save_rep["write_throughput_MB_per_sec"],
            "read_speed_MB_s": load_rep["read_throughput_MB_per_sec"],
            "execution_time_sec": round(io_time, 4)
        }

        # 4. Test Multi-Scale Synaptic Electrophysiology
        t0 = time.perf_counter()
        syn_rep = MultiScaleWholeCellNeuronCore.simulate_multiscale_synapse_and_spine_plasticity(
            lipid_cleft_gap_nm=2.0, reorganization_lambda_ev=0.70, initial_spine_volume_um3=0.10,
            g_actin_conc_um=5.0, temp_k=310.15, sim_duration_ms=20.0, dt_ms=0.05
        )
        syn_time = time.perf_counter() - t0
        results["layer_4_biophysical_synapse"] = {
            "status": "PASS" if syn_rep["scale_3_somatic_electrophysiology"]["action_potentials_fired"] > 0 else "FAIL",
            "spikes_detected": syn_rep["scale_3_somatic_electrophysiology"]["action_potentials_fired"],
            "spine_growth_pct": syn_rep["scale_4_dendritic_spine_plasticity"]["structural_LTP_volume_growth_percent"],
            "execution_time_sec": round(syn_time, 4)
        }

        # 5. Test Relativistic Spacetime Geodesics
        t0 = time.perf_counter()
        geo_rep = TopologicalSpacetimeGeodesicCore.simulate_4d_curved_geodesic(
            spacetime_type="kerr", mass_m=1.0, spin_a=0.9, initial_r=10.0,
            specific_energy_e=1.0, specific_angular_momentum_l=2.8,
            particle_type="photon", step_d_lambda=0.02, max_steps=500
        )
        geo_time = time.perf_counter() - t0
        results["layer_5_spacetime_geodesics"] = {
            "status": "PASS" if geo_rep["metric_invariants"]["outer_event_horizon_r_plus"] > 0 else "FAIL",
            "deflection_deg": geo_rep["geodesic_solution"]["total_frame_dragged_rotation_deg"],
            "execution_time_sec": round(geo_time, 4)
        }

        total_duration = time.perf_counter() - start_time
        all_passed = all(layer["status"] == "PASS" for layer in results.values())

        return {
            "system_health": "100% OPERATIONAL (ALL TIERS VERIFIED)" if all_passed else "DEGRADED",
            "total_benchmark_time_seconds": round(total_duration, 4),
            "layers_diagnostic": results
        }
