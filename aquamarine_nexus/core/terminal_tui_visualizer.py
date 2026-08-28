import math
from typing import List, Dict, Any, Tuple

class TerminalTUIVisualizerCore:
    # ANSI Escape Codes for Styling
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"
    RED = "\033[31m"

    @staticmethod
    def render_ascii_curve(
        data_points: List[float],
        title: str = "AQUAMARINE NEXUS INVARIANT FLOW",
        width: int = 60,
        height: int = 15,
        y_unit: str = "mV"
    ) -> str:
        """
        Renders a high-resolution 2D line plot directly in the terminal using pure ASCII/ANSI blocks.
        """
        if not data_points or len(data_points) < 2:
            raise ValueError("At least 2 data points required for curve rendering.")

        min_val = min(data_points)
        max_val = max(data_points)
        val_range = max_val - min_val if max_val != min_val else 1.0

        # Resample data points to fit console width
        resampled = []
        n_pts = len(data_points)
        for col in range(width):
            src_idx = int(col * (n_pts - 1) / (width - 1))
            resampled.append(data_points[src_idx])

        # Initialize canvas grid
        canvas = [[" " for _ in range(width)] for _ in range(height)]

        for col, val in enumerate(resampled):
            # Normalize to row index [0, height - 1] (inverted because row 0 is top)
            normalized_y = (val - min_val) / val_range
            row = height - 1 - int(normalized_y * (height - 1))
            row = max(0, min(height - 1, row))
            canvas[row][col] = "█"

        # Build output string with ANSI border and axis labels
        lines = []
        border_top = f"{TerminalTUIVisualizerCore.CYAN}┌" + "─" * (width + 12) + f"┐{TerminalTUIVisualizerCore.RESET}"
        title_line = f"{TerminalTUIVisualizerCore.CYAN}│{TerminalTUIVisualizerCore.RESET} {TerminalTUIVisualizerCore.BOLD}{TerminalTUIVisualizerCore.MAGENTA}{title.center(width + 10)}{TerminalTUIVisualizerCore.RESET} {TerminalTUIVisualizerCore.CYAN}│{TerminalTUIVisualizerCore.RESET}"
        divider = f"{TerminalTUIVisualizerCore.CYAN}├" + "─" * (width + 12) + f"┤{TerminalTUIVisualizerCore.RESET}"
        
        lines.append(border_top)
        lines.append(title_line)
        lines.append(divider)

        for r in range(height):
            # Y-axis value calculation for this row
            row_val = max_val - (r / (height - 1)) * val_range
            y_label = f"{row_val:7.2f} {y_unit:>2} │"
            row_str = "".join(
                f"{TerminalTUIVisualizerCore.GREEN}{ch}{TerminalTUIVisualizerCore.RESET}" if ch == "█" else ch 
                for ch in canvas[r]
            )
            lines.append(f"{TerminalTUIVisualizerCore.CYAN}│{TerminalTUIVisualizerCore.RESET} {TerminalTUIVisualizerCore.YELLOW}{y_label}{TerminalTUIVisualizerCore.RESET} {row_str} {TerminalTUIVisualizerCore.CYAN}│{TerminalTUIVisualizerCore.RESET}")

        border_bottom = f"{TerminalTUIVisualizerCore.CYAN}└" + "─" * (width + 12) + f"┘{TerminalTUIVisualizerCore.RESET}"
        lines.append(border_bottom)

        return "\n".join(lines)

    @staticmethod
    def render_2d_trajectory_phase_map(
        x_points: List[float],
        y_points: List[float],
        title: str = "4D SPACETIME GEODESIC / PHASE MAP",
        size: int = 25
    ) -> str:
        """
        Renders a 2D spatial trajectory / phase portrait using matrix grid mapping.
        """
        if len(x_points) != len(y_points) or not x_points:
            raise ValueError("X and Y trajectory coordinates must be non-empty and matching in size.")

        min_x, max_x = min(x_points), max(x_points)
        min_y, max_y = min(y_points), max(y_points)

        span_x = max_x - min_x if max_x != min_x else 1.0
        span_y = max_y - min_y if max_y != min_y else 1.0

        grid = [["·" for _ in range(size)] for _ in range(size)]

        for x_val, y_val in zip(x_points, y_points):
            col = int(((x_val - min_x) / span_x) * (size - 1))
            row = size - 1 - int(((y_val - min_y) / span_y) * (size - 1))
            row = max(0, min(size - 1, row))
            col = max(0, min(size - 1, col))
            grid[row][col] = "●"

        # Center indicator (Singularity / Origin)
        center_row = size // 2
        center_col = size // 2
        if grid[center_row][center_col] == "·":
            grid[center_row][center_col] = "⊕"

        rendered_rows = []
        rendered_rows.append(f"{TerminalTUIVisualizerCore.CYAN}╔" + "═" * (size * 2 + 2) + f"╗{TerminalTUIVisualizerCore.RESET}")
        rendered_rows.append(f"{TerminalTUIVisualizerCore.CYAN}║{TerminalTUIVisualizerCore.RESET} {TerminalTUIVisualizerCore.BOLD}{TerminalTUIVisualizerCore.MAGENTA}{title.center(size * 2)}{TerminalTUIVisualizerCore.RESET} {TerminalTUIVisualizerCore.CYAN}║{TerminalTUIVisualizerCore.RESET}")
        rendered_rows.append(f"{TerminalTUIVisualizerCore.CYAN}╠" + "═" * (size * 2 + 2) + f"╣{TerminalTUIVisualizerCore.RESET}")

        for row in grid:
            formatted_row = " ".join(
                f"{TerminalTUIVisualizerCore.RED}⊕{TerminalTUIVisualizerCore.RESET}" if ch == "⊕" else
                f"{TerminalTUIVisualizerCore.GREEN}●{TerminalTUIVisualizerCore.RESET}" if ch == "●" else
                f"\033[90m·\033[0m" for ch in row
            )
            rendered_rows.append(f"{TerminalTUIVisualizerCore.CYAN}║{TerminalTUIVisualizerCore.RESET} {formatted_row} {TerminalTUIVisualizerCore.CYAN}║{TerminalTUIVisualizerCore.RESET}")

        rendered_rows.append(f"{TerminalTUIVisualizerCore.CYAN}╚" + "═" * (size * 2 + 2) + f"╝{TerminalTUIVisualizerCore.RESET}")
        return "\n".join(rendered_rows)
