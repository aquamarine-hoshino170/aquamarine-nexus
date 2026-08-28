# 🌌 Aquamarine Nexus — Complete Scientific Catalog

> Auto-generated ecosystem reference and mathematical registry.

| Command / Engine | Type Signature | Scientific Description |
| :--- | :--- | :--- |
| `acceleration_1d` | `(christoffel_gamma: float, velocity: float) -> dict` | Geodesic equation: d^2x/dt^2 + Gamma * (dx/dt)^2 = 0 |
| `adaptive_simpson_integral` | `(func, a: float, b: float, n: int = 1000) -> float` | Composite Simpson's 1/3 Rule for Numerical Integration |
| `alfven_velocity` | `(b_field_tesla: float, plasma_mass_density_kg_m3: float) -> dict` | Computes Alfvén wave phase velocity: v_A = B / sqrt(mu_0 * rho) |
| `area_preservation` | `(q_spread: float, p_spread: float) -> dict` | Liouville's theorem invariant: Area = Delta_q * Delta_p |
| `automated_tests` | `(output_path='tests/test_auto.py')` | Core numerical routine |
| `bell_state_amplitudes` | `(state_name: str) -> dict` | Returns basis state amplitudes for the 4 maximally entangled 2-qubit Bell states: |
| `berry_curvature` | `(kx: float, ky: float, mass_gap: float = 1.0, v_fermi: float = 1.0) -> dict` | Computes Berry curvature Omega_z(k) for massive Dirac 2-band Hamiltonian: |
| `binary_chirp_mass` | `(m1_kg: float, m2_kg: float) -> dict` | Computes Chirp Mass M_chirp = (m1 * m2)^(3/5) / (m1 + m2)^(1/5) |
| `bloch_vector_from_state` | `(alpha_real: float, alpha_imag: float, beta_real: float, beta_imag: float) -> dict` | Converts pure qubit state \|psi> = alpha\|0> + beta\|1> to Bloch coordinates (u, v, w): |
| `bose_einstein_distribution` | `(energy_ev: float, chemical_potential_ev: float, temp_k: float) -> dict` | Bose-Einstein statistics: n(E) = 1 / (exp((E - mu) / (k_B * T)) - 1) |
| `brownian_step` | `(s_current: float, mu_drift: float, sigma_volatility: float, z_normal: float, dt: float) -> dict` | Analytic step for Geometric Brownian Motion (Itô Calculus): |
| `call_dredge_engine` | `(engine_name: str, *params)` | Core numerical routine |
| `chirp_mass` | `(m1_kg: float, m2_kg: float) -> dict` | Computes Chirp Mass M_chirp = (m1 * m2)^(3/5) / (m1 + m2)^(1/5) |
| `christoffel_1d` | `(g_func, x: float, h: float = 1e-05) -> float` | Christoffel Symbol Calculation for 1D Metric Tensor: Γ = 1/2 * g^-1 * (dg/dx) |
| `chsh_inequality_correlation` | `(theta_a: float, theta_a_prime: float, theta_b: float, theta_b_prime: float) -> dict` | Computes CHSH parameter S = E(a,b) - E(a,b') + E(a',b) + E(a',b') for singlet state \|psi_minus>. |
| `compton_wavelength` | `(rest_mass_kg: float) -> dict` | Calculates Compton Wavelength lambda_c = h / (m * c)  |
| `contour_residue_pole_simple` | `(func, z0: complex, r: float = 0.0001, points: int = 128) -> complex` | Numerical Residue via Cauchy's Integral Formula |
| `conversion_efficiency` | `(delta_k_rad_m: float, crystal_length_m: float, d_eff_pm_v: float = 2.0) -> dict` | Phase-matching sinc^2 function for Second Harmonic Generation (SHG): |
| `convolve_1d` | `(signal: list, kernel: list) -> list` | 1D Discrete Linear Convolution (y = x * h) |
| `covariant_derivative_scalar_field` | `(df_dx: float) -> dict` | For a scalar field, covariant derivative is simply the partial derivative: grad(phi)_i = d(phi)/dx^i |
| `d2q9_equilibrium_density` | `(rho: float, ux: float, uy: float) -> dict` | Computes 9 discrete equilibrium distribution functions f_i^(eq) for D2Q9 lattice: |
| `debye_length` | `(electron_density_m3: float, electron_temp_k: float) -> dict` | Computes Debye Screening Length lambda_D = sqrt( (eps_0 * k_B * T_e) / (n_e * e^2) ) |
| `density_profile` | `(radius_kpc: float, scale_radius_rs_kpc: float, rho_0_msun_kpc3: float) -> dict` | Navarro-Frenk-White (NFW) Dark Matter Density Profile: |
| `det_2x2` | `(matrix: list)` | Core numerical routine |
| `dft_1d` | `(signal: list) -> list` | Pure-Python Discrete Fourier Transform: |
| `dijkstra_shortest_path` | `(nodes: list, edges: list, start_node, target_node) -> dict` | Computes shortest path on weighted graph: edges = [(u, v, weight), ...] |
| `dirac_distribution` | `(energy_ev: float, fermi_energy_ev: float, temp_k: float) -> dict` | Fermi-Dirac statistics: f(E) = 1 / (exp((E - E_F) / (k_B * T)) + 1) |
| `dirac_probability_density` | `(psi_0_real: float, psi_0_imag: float, psi_1_real: float, psi_1_imag: float, psi_2_real: float, psi_2_imag: float, psi_3_real: float, psi_3_imag: float) -> dict` | Computes the conserved probability density J^0 = psi_dagger * psi for a 4-component Dirac spinor. |
| `discrete_convolve_1d` | `(signal: list, kernel: list) -> list` | 1D Discrete Linear Convolution (y = x * h) |
| `dredge` | `(engine_name: str, *params)` | Core numerical routine |
| `dredge_engine` | `(engine_name: str, *params)` | Core numerical routine |
| `eddington_luminosity` | `(mass_kg: float) -> dict` | Computes Eddington Critical Accretion Luminosity: |
| `einstein_distribution` | `(energy_ev: float, chemical_potential_ev: float, temp_k: float) -> dict` | Bose-Einstein statistics: n(E) = 1 / (exp((E - mu) / (k_B * T)) - 1) |
| `elementary_step` | `(state: list, rule_number: int) -> list` | Executes one step of 1D Elementary Cellular Automaton (e.g., Rule 30, 110). |
| `entropy_production` | `(l_matrix: list, thermodynamic_forces: list) -> dict` | Computes thermodynamic fluxes J_i = sum_j (L_ij * X_j)  |
| `equilibrium_density` | `(rho: float, ux: float, uy: float) -> dict` | Computes 9 discrete equilibrium distribution functions f_i^(eq) for D2Q9 lattice: |
| `ergosphere_radius` | `(mass_kg: float, spin_param_a: float, theta_rad: float) -> dict` | Calculates Kerr Ergosphere Outer Boundary in Boyer-Lindquist coordinates: |
| `excited_state_inversion` | `(time_seconds: float, coupling_g_hz: float, photon_number_n: int = 0) -> dict` | Calculates atomic inversion W(t) = -cos(Omega_n * t) for resonant excitation (Delta = 0) starting in \|e, n> |
| `expansion_exp` | `(x: float, order: int = 10) -> dict` | Symbolic-numeric Taylor series for e^x = sum(x^k / k!) |
| `expansion_sin` | `(x: float, order: int = 5) -> dict` | Taylor series for sin(x) = sum((-1)^k * x^(2k+1) / (2k+1)!) |
| `export_csv` | `(matrix: list, filepath: str) -> dict` | Exports a 2D matrix/table to CSV |
| `export_json` | `(data: dict, filepath: str) -> dict` | Exports dictionary or computational state to a JSON file |
| `export_serialized` | `(obj, filepath: str) -> dict` | Serializes any Python object/state into an encrypted Base64 string payload |
| `extended_gcd` | `(a: int, b: int)` | Extended Euclidean Algorithm: returns (gcd, x, y) such that ax + by = gcd |
| `eye` | `(n: int)` | Core numerical routine |
| `fermi_dirac_distribution` | `(energy_ev: float, fermi_energy_ev: float, temp_k: float) -> dict` | Fermi-Dirac statistics: f(E) = 1 / (exp((E - E_F) / (k_B * T)) + 1) |
| `from_state` | `(alpha_real: float, alpha_imag: float, beta_real: float, beta_imag: float) -> dict` | Converts pure qubit state \|psi> = alpha\|0> + beta\|1> to Bloch coordinates (u, v, w): |
| `game_of_life_step` | `(grid: list) -> list` | Executes one tick of Conway's Game of Life on a 2D toroidal lattice grid. |
| `gaussian_and_mean_curvature` | `(e: float, f: float, g: float, l: float, m: float, n: float) -> dict` | Computes Gaussian Curvature (K) and Mean Curvature (H) given: |
| `generate_automated_tests` | `(output_path='tests/test_auto.py')` | Core numerical routine |
| `generate_markdown_docs` | `(output_path='DOCS.md')` | Core numerical routine |
| `geodesic_acceleration_1d` | `(christoffel_gamma: float, velocity: float) -> dict` | Geodesic equation: d^2x/dt^2 + Gamma * (dx/dt)^2 = 0 |
| `geometric_brownian_step` | `(s_current: float, mu_drift: float, sigma_volatility: float, z_normal: float, dt: float) -> dict` | Analytic step for Geometric Brownian Motion (Itô Calculus): |
| `glauert_correction` | `(incompressible_cp: float, mach_number: float) -> dict` | Prandtl-Glauert compressibility correction for subsonic flow: |
| `golden_section_minimize` | `(func, a: float, b: float, tol: float = 1e-06) -> dict` | Golden-section search for 1D scalar function minimization on [a, b] |
| `graph_laplacian_spectrum_2x2` | `(deg_matrix: list, adj_matrix: list) -> list` | Computes Graph Laplacian L = D - A for 2x2 graph |
| `gray_scott_point_step` | `(u: float, v: float, f_feed: float = 0.055, k_kill: float = 0.062, dt: float = 1.0) -> dict` | Calculates local chemical reaction for Morphogens: |
| `gw_quadrupole_power` | `(m1_kg: float, m2_kg: float, separation_r_m: float) -> dict` | Peters-Mathews Quadrupole Formula: Radiated Gravitational Wave Power |
| `hall_conductance` | `(chern_number_c: int) -> dict` | TKNN Formula: Quantized Hall Conductance sigma_xy = C * (e^2 / h) |
| `harmonic_oscillator_symplectic_step` | `(q: float, p: float, dt: float, m: float = 1.0, k: float = 1.0) -> dict` | Symplectic Euler integrator for H(q, p) = p^2/(2m) + (1/2)k*q^2: |
| `hawking_thermodynamics` | `(mass_kg: float) -> dict` | Computes Event Horizon Area (A), Hawking Temperature (T_H), and Bekenstein-Hawking Entropy (S_BH): |
| `import_csv` | `(filepath: str) -> list` | Imports CSV file into a 2D matrix of numeric floats/strings |
| `import_json` | `(filepath: str) -> dict` | Imports computational state from a JSON file |
| `import_serialized` | `(filepath: str)` | Deserializes object from Base64 encoded payload file |
| `inequality_correlation` | `(theta_a: float, theta_a_prime: float, theta_b: float, theta_b_prime: float) -> dict` | Computes CHSH parameter S = E(a,b) - E(a,b') + E(a',b) + E(a',b') for singlet state \|psi_minus>. |
| `instability_mass` | `(density_kg_m3: float, gas_temp_k: float, mean_molecular_weight: float = 1.0) -> dict` | Computes Jeans Length (lambda_J) and Jeans Critical Mass (M_J) for gravitational collapse: |
| `invariant_mass` | `(total_energy_joules: float, px: float, py: float, pz: float) -> dict` | Computes invariant rest mass: |
| `iteration_eigen` | `(A: list, num_iter: int = 50) -> dict` | Computes dominant eigenvalue and eigenvector |
| `jeans_instability_mass` | `(density_kg_m3: float, gas_temp_k: float, mean_molecular_weight: float = 1.0) -> dict` | Computes Jeans Length (lambda_J) and Jeans Critical Mass (M_J) for gravitational collapse: |
| `joukowsky_transform` | `(real: float, imag: float) -> dict` | Joukowsky Aerodynamic Conformal Mapping: w = z + 1/z |
| `kdv_single_soliton` | `(x: float, t: float, velocity: float) -> dict` | KdV 1-Soliton analytical profile: |
| `kerr_ergosphere_radius` | `(mass_kg: float, spin_param_a: float, theta_rad: float) -> dict` | Calculates Kerr Ergosphere Outer Boundary in Boyer-Lindquist coordinates: |
| `kerr_refractive_index` | `(n0: float, n2_m2_w: float, intensity_w_m2: float) -> dict` | Optical Kerr Effect: n(I) = n0 + n2 * I |
| `kmeans_1d` | `(data: list, k: int = 2, max_iters: int = 20) -> dict` | 1D K-Means Clustering |
| `larmor_radiation_power` | `(charge_coulomb: float, acceleration_m_s2: float) -> dict` | Larmor Formula: Total power radiated by an accelerating non-relativistic point charge: |
| `lempel_ziv_complexity` | `(binary_string: str) -> dict` | Computes Lempel-Ziv (LZ76) algorithmic complexity for binary/symbolic strings. |
| `life_step` | `(grid: list) -> list` | Executes one tick of Conway's Game of Life on a 2D toroidal lattice grid. |
| `linear_regression_1d` | `(x_vals: list, y_vals: list) -> dict` | Ordinary Least Squares (OLS) Linear Regression: y = m*x + c |
| `logistic_map_lyapunov` | `(r: float, x0: float = 0.5, steps: int = 500) -> dict` | Computes Lyapunov Exponent lambda for Logistic Map: x_{n+1} = r * x * (1 - x) |
| `lorenz_rk4_step` | `(x: float, y: float, z: float, dt: float = 0.01, sigma: float = 10.0, rho: float = 28.0, beta: float = 2.6666666666666665) -> dict` | Integrates Lorenz ODEs by one step dt via Runge-Kutta 4th Order: |
| `lu_decompose` | `(A: list)` | Doolittle Algorithm for LU Decomposition (A = L * U) |
| `mandelbrot_escape` | `(c_real: float, c_imag: float, max_iter: int = 100) -> dict` | Computes escape iteration count for z_{n+1} = z_n^2 + c in complex plane |
| `map_lyapunov` | `(r: float, x0: float = 0.5, steps: int = 500) -> dict` | Computes Lyapunov Exponent lambda for Logistic Map: x_{n+1} = r * x * (1 - x) |
| `markdown_docs` | `(output_path='DOCS.md')` | Core numerical routine |
| `matmul` | `(A: list, B: list) -> list` | Core numerical routine |
| `matrix_det_2x2` | `(matrix: list)` | Core numerical routine |
| `matrix_inverse` | `(A: list) -> list` | Invert matrix using LU Back-substitution |
| `matrix_mul` | `(A: list, B: list)` | Core numerical routine |
| `mean_curvature` | `(e: float, f: float, g: float, l: float, m: float, n: float) -> dict` | Computes Gaussian Curvature (K) and Mean Curvature (H) given: |
| `metric_tensor_2d` | `(g11: float, g12: float, g22: float) -> dict` | 2D Metric Tensor analysis: determinant and inverse components |
| `metric_tensor_christoffel_1d` | `(g_func, x: float, h: float = 1e-05) -> float` | Christoffel Symbol Calculation for 1D Metric Tensor: Γ = 1/2 * g^-1 * (dg/dx) |
| `mobius_sl2r_transform` | `(a: float, b: float, c: float, d: float, z_real: float, z_imag: float) -> dict` | Möbius isometry f(z) = (az + b) / (cz + d) in SL(2, R) where ad - bc = 1 |
| `molecular_weight` | `(formula: str) -> dict` | Calculates molecular mass and mass fraction of elements |
| `neuron_spike_step` | `(v: float, w: float, i_ext: float = 0.5, a: float = 0.7, b: float = 0.8, tau: float = 12.5, dt: float = 0.1) -> dict` | Integrates membrane voltage (v) and recovery variable (w): |
| `nfw_density_profile` | `(radius_kpc: float, scale_radius_rs_kpc: float, rho_0_msun_kpc3: float) -> dict` | Navarro-Frenk-White (NFW) Dark Matter Density Profile: |
| `normal_shock_relations` | `(mach_1: float, gamma: float = 1.4) -> dict` | Computes downstream properties across a normal shock wave given upstream Mach number M1 > 1. |
| `numerical_derivative` | `(func, x: float, h: float = 1e-07) -> float` | Central Difference Method (O(h^2) accuracy) |
| `ode_step` | `(func, t: float, y: float, dt: float) -> float` | Runge-Kutta 4th Order ODE Step |
| `onsager_flux_and_entropy_production` | `(l_matrix: list, thermodynamic_forces: list) -> dict` | Computes thermodynamic fluxes J_i = sum_j (L_ij * X_j)  |
| `oscillation_frequency` | `(coupling_strength_g_hz: float, detuning_delta_hz: float = 0.0, photon_number_n: int = 0) -> dict` | Computes generalized Jaynes-Cummings Rabi Frequency: |
| `parse_formula` | `(formula: str) -> dict` | Parses chemical formula e.g. C6H12O6, H2SO4, Fe2O3 |
| `parse_value_with_type` | `(val_str: str, expected_type)` | Core numerical routine |
| `pauli_spin_expectation` | `(alpha_real: float, alpha_imag: float, beta_real: float, beta_imag: float) -> dict` | Computes expectation values <sigma_x>, <sigma_y>, <sigma_z> for state \|psi> = alpha\|0> + beta\|1> |
| `phase_space_area_preservation` | `(q_spread: float, p_spread: float) -> dict` | Liouville's theorem invariant: Area = Delta_q * Delta_p |
| `plane_distance` | `(z1_real: float, z1_imag: float, z2_real: float, z2_imag: float) -> dict` | Hyperbolic distance d(z1, z2) in Upper Half-Plane H^2: |
| `poincare_half_plane_distance` | `(z1_real: float, z1_imag: float, z2_real: float, z2_imag: float) -> dict` | Hyperbolic distance d(z1, z2) in Upper Half-Plane H^2: |
| `point_step` | `(u: float, v: float, f_feed: float = 0.055, k_kill: float = 0.062, dt: float = 1.0) -> dict` | Calculates local chemical reaction for Morphogens: |
| `pole_simple` | `(func, z0: complex, r: float = 0.0001, points: int = 128) -> complex` | Numerical Residue via Cauchy's Integral Formula |
| `poly_add` | `(p1: list, p2: list) -> list` | Adds two polynomials represented as coefficient lists |
| `poly_derivative` | `(poly_coeffs: list) -> list` | Differentiates polynomial represented by coefficient list [a_0, a_1, a_2, ...] (a0 + a1*x + a2*x^2) |
| `poly_eval` | `(coeffs: list, x: float) -> float` | Evaluates P(x) = c0 + c1*x + c2*x^2 + ... via Horner's Method |
| `poly_mul` | `(p1: list, p2: list) -> list` | Multiplies two polynomials (Cauchy Product) |
| `power_iteration_eigen` | `(A: list, num_iter: int = 50) -> dict` | Computes dominant eigenvalue and eigenvector |
| `poynting_vector` | `(e_field_v_m: list, b_field_tesla: list) -> dict` | Calculates Poynting Vector S = (E x B) / mu_0 |
| `prandtl_glauert_correction` | `(incompressible_cp: float, mach_number: float) -> dict` | Prandtl-Glauert compressibility correction for subsonic flow: |
| `prime_factorization` | `(n: int) -> dict` | Core numerical routine |
| `probability_density` | `(psi_0_real: float, psi_0_imag: float, psi_1_real: float, psi_1_imag: float, psi_2_real: float, psi_2_imag: float, psi_3_real: float, psi_3_imag: float) -> dict` | Computes the conserved probability density J^0 = psi_dagger * psi for a 4-component Dirac spinor. |
| `purity_2x2` | `(rho_00: float, rho_01_real: float, rho_01_imag: float, rho_11: float) -> dict` | Computes purity gamma = Tr(rho^2) for a 2x2 density matrix |
| `quadrupole_power` | `(m1_kg: float, m2_kg: float, separation_r_m: float) -> dict` | Peters-Mathews Quadrupole Formula: Radiated Gravitational Wave Power |
| `quantum_hall_conductance` | `(chern_number_c: int) -> dict` | TKNN Formula: Quantized Hall Conductance sigma_xy = C * (e^2 / h) |
| `qubit_purity_2x2` | `(rho_00: float, rho_01_real: float, rho_01_imag: float, rho_11: float) -> dict` | Computes purity gamma = Tr(rho^2) for a 2x2 density matrix |
| `rabi_oscillation_frequency` | `(coupling_strength_g_hz: float, detuning_delta_hz: float = 0.0, photon_number_n: int = 0) -> dict` | Computes generalized Jaynes-Cummings Rabi Frequency: |
| `radiation_power` | `(charge_coulomb: float, acceleration_m_s2: float) -> dict` | Larmor Formula: Total power radiated by an accelerating non-relativistic point charge: |
| `refractive_index` | `(n0: float, n2_m2_w: float, intensity_w_m2: float) -> dict` | Optical Kerr Effect: n(I) = n0 + n2 * I |
| `regression_1d` | `(x_vals: list, y_vals: list) -> dict` | Ordinary Least Squares (OLS) Linear Regression: y = m*x + c |
| `relativistic_doppler` | `(source_freq_hz: float, velocity_m_s: float, theta_rad: float = 0.0) -> dict` | Relativistic Doppler frequency shift: |
| `relativistic_invariant_mass` | `(total_energy_joules: float, px: float, py: float, pz: float) -> dict` | Computes invariant rest mass: |
| `reverse_complement` | `(dna_seq: str) -> str` | Core numerical routine |
| `rk4_ode_step` | `(func, t: float, y: float, dt: float) -> float` | Runge-Kutta 4th Order ODE Step |
| `rk4_step` | `(x: float, y: float, z: float, dt: float = 0.01, sigma: float = 10.0, rho: float = 28.0, beta: float = 2.6666666666666665) -> dict` | Integrates Lorenz ODEs by one step dt via Runge-Kutta 4th Order: |
| `scalar_field` | `(df_dx: float) -> dict` | For a scalar field, covariant derivative is simply the partial derivative: grad(phi)_i = d(phi)/dx^i |
| `section_minimize` | `(func, a: float, b: float, tol: float = 1e-06) -> dict` | Golden-section search for 1D scalar function minimization on [a, b] |
| `shg_conversion_efficiency` | `(delta_k_rad_m: float, crystal_length_m: float, d_eff_pm_v: float = 2.0) -> dict` | Phase-matching sinc^2 function for Second Harmonic Generation (SHG): |
| `shock_relations` | `(mach_1: float, gamma: float = 1.4) -> dict` | Computes downstream properties across a normal shock wave given upstream Mach number M1 > 1. |
| `shortest_path` | `(nodes: list, edges: list, start_node, target_node) -> dict` | Computes shortest path on weighted graph: edges = [(u, v, weight), ...] |
| `simpson_integral` | `(func, a: float, b: float, n: int = 1000) -> float` | Composite Simpson's 1/3 Rule for Numerical Integration |
| `single_soliton` | `(x: float, t: float, velocity: float) -> dict` | KdV 1-Soliton analytical profile: |
| `sl2r_transform` | `(a: float, b: float, c: float, d: float, z_real: float, z_imag: float) -> dict` | Möbius isometry f(z) = (az + b) / (cz + d) in SL(2, R) where ad - bc = 1 |
| `spacetime_interval` | `(dt_s: float, dx_m: float, dy_m: float, dz_m: float) -> dict` | Minkowski invariant interval: |
| `spectrum_2x2` | `(deg_matrix: list, adj_matrix: list) -> list` | Computes Graph Laplacian L = D - A for 2x2 graph |
| `spike_step` | `(v: float, w: float, i_ext: float = 0.5, a: float = 0.7, b: float = 0.8, tau: float = 12.5, dt: float = 0.1) -> dict` | Integrates membrane voltage (v) and recovery variable (w): |
| `spin_expectation` | `(alpha_real: float, alpha_imag: float, beta_real: float, beta_imag: float) -> dict` | Computes expectation values <sigma_x>, <sigma_y>, <sigma_z> for state \|psi> = alpha\|0> + beta\|1> |
| `state_amplitudes` | `(state_name: str) -> dict` | Returns basis state amplitudes for the 4 maximally entangled 2-qubit Bell states: |
| `state_inversion` | `(time_seconds: float, coupling_g_hz: float, photon_number_n: int = 0) -> dict` | Calculates atomic inversion W(t) = -cos(Omega_n * t) for resonant excitation (Delta = 0) starting in \|e, n> |
| `step_state` | `(theta1: float, theta2: float, omega1: float, omega2: float, m1: float = 1.0, m2: float = 1.0, l1: float = 1.0, l2: float = 1.0, g: float = 9.80665, dt: float = 0.01) -> dict` | Calculates angular accelerations (alpha1, alpha2) and integrates 1 time-step dt. |
| `stereographic_projection` | `(x: float, y: float) -> dict` | Projects point (x, y) on the complex plane onto the unit Riemann Sphere (X, Y, Z): |
| `symbolic_poly_derivative` | `(poly_coeffs: list) -> list` | Differentiates polynomial represented by coefficient list [a_0, a_1, a_2, ...] (a0 + a1*x + a2*x^2) |
| `symplectic_step` | `(q: float, p: float, dt: float, m: float = 1.0, k: float = 1.0) -> dict` | Symplectic Euler integrator for H(q, p) = p^2/(2m) + (1/2)k*q^2: |
| `taylor_expansion_exp` | `(x: float, order: int = 10) -> dict` | Symbolic-numeric Taylor series for e^x = sum(x^k / k!) |
| `taylor_expansion_sin` | `(x: float, order: int = 5) -> dict` | Taylor series for sin(x) = sum((-1)^k * x^(2k+1) / (2k+1)!) |
| `tensor_2d` | `(g11: float, g12: float, g22: float) -> dict` | 2D Metric Tensor analysis: determinant and inverse components |
| `transcribe` | `(dna_seq: str) -> str` | DNA to mRNA transcription (T -> U) |
| `translate` | `(dna_seq: str) -> dict` | Translates DNA sequence into Amino Acid Polypeptide Chain |
| `two_band_berry_curvature` | `(kx: float, ky: float, mass_gap: float = 1.0, v_fermi: float = 1.0) -> dict` | Computes Berry curvature Omega_z(k) for massive Dirac 2-band Hamiltonian: |
| `van_der_waals_pressure` | `(temp_k: float, molar_volume_m3_mol: float, a_param: float, b_param: float) -> dict` | Computes real gas pressure: |
| `waals_pressure` | `(temp_k: float, molar_volume_m3_mol: float, a_param: float, b_param: float) -> dict` | Computes real gas pressure: |
| `wiener_variance` | `(t_time: float) -> dict` | Wiener process property: Var(W_t) = t, Mean(W_t) = 0 |
| `with_type` | `(val_str: str, expected_type)` | Core numerical routine |
| `wolfram_elementary_step` | `(state: list, rule_number: int) -> list` | Executes one step of 1D Elementary Cellular Automaton (e.g., Rule 30, 110). |
| `zeros` | `(rows: int, cols: int)` | Core numerical routine |
| `ziv_complexity` | `(binary_string: str) -> dict` | Computes Lempel-Ziv (LZ76) algorithmic complexity for binary/symbolic strings. |
