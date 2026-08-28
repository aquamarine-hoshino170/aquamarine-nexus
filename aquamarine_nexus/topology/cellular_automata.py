class CellularAutomataCore:
    """Discrete Dynamical Systems & Wolfram/Conway Lattice Topologies"""

    @staticmethod
    def wolfram_elementary_step(state: list, rule_number: int) -> list:
        """
        Executes one step of 1D Elementary Cellular Automaton (e.g., Rule 30, 110).
        state: binary array e.g. [0, 1, 0]
        """
        if not (0 <= rule_number <= 255):
            raise ValueError("Rule number must be in range 0-255.")
        
        rule_bin = f"{rule_number:08b}"
        lookup = {
            (1, 1, 1): int(rule_bin[0]),
            (1, 1, 0): int(rule_bin[1]),
            (1, 0, 1): int(rule_bin[2]),
            (1, 0, 0): int(rule_bin[3]),
            (0, 1, 1): int(rule_bin[4]),
            (0, 1, 0): int(rule_bin[5]),
            (0, 0, 1): int(rule_bin[6]),
            (0, 0, 0): int(rule_bin[7]),
        }
        n = len(state)
        next_state = [0] * n
        for i in range(n):
            neighborhood = (state[(i - 1) % n], state[i], state[(i + 1) % n])
            next_state[i] = lookup[neighborhood]
        return next_state

    @staticmethod
    def game_of_life_step(grid: list) -> list:
        """
        Executes one tick of Conway's Game of Life on a 2D toroidal lattice grid.
        grid: 2D matrix of 0s and 1s
        """
        rows = len(grid)
        cols = len(grid[0])
        next_grid = [[0 for _ in range(cols)] for _ in range(rows)]

        for r in range(rows):
            for c in range(cols):
                live_neighbors = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr = (r + dr) % rows
                        nc = (c + dc) % cols
                        live_neighbors += grid[nr][nc]

                if grid[r][c] == 1:
                    next_grid[r][c] = 1 if live_neighbors in (2, 3) else 0
                else:
                    next_grid[r][c] = 1 if live_neighbors == 3 else 0

        return next_grid
