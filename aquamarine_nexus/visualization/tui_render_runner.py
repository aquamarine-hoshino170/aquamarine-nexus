import math
from aquamarine_nexus.core.terminal_tui_visualizer import TerminalTUIVisualizerCore

class TUIRenderRunnerCore:
    @staticmethod
    def visualize_hodgkin_huxley_spikes() -> str:
        """Generates synthetic multi-spike action potential wave and prints high-res TUI curve."""
        t_steps = 120
        wave = []
        for i in range(t_steps):
            t = i * 0.4
            v = -65.0
            for t_spike in [10.0, 25.0, 40.0]:
                if t >= t_spike:
                    dt = t - t_spike
                    if dt < 6.0:
                        v += 105.0 * (dt / 1.2) * math.exp(1.0 - (dt / 1.2))
            wave.append(v)

        return TerminalTUIVisualizerCore.render_ascii_curve(
            wave,
            title="NEURONAL SOMATIC ACTION POTENTIAL TRAIN",
            width=55,
            height=12,
            y_unit="mV"
        )

    @staticmethod
    def visualize_kerr_blackhole_orbit() -> str:
        """Generates Kerr equatorial photon trajectory coordinates and renders 2D phase map."""
        x_coords = []
        y_coords = []
        
        for step in range(150):
            phi = step * 0.12
            r = 10.0 * math.exp(-0.012 * step)
            x_coords.append(r * math.cos(phi))
            y_coords.append(r * math.sin(phi))

        return TerminalTUIVisualizerCore.render_2d_trajectory_phase_map(
            x_coords,
            y_coords,
            title="KERR PHOTON ORBIT & LENSING MAP",
            size=21
        )
