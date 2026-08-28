import sys
import os
import tty
import termios
from aquamarine_nexus.core.advanced_symbolic_cas import AdvancedSymbolicCAS
from aquamarine_nexus.core.aqua_binary_serializer import AquaBinaryProtocol

class AquaTerminalEditor:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    MAGENTA = "\033[35m"
    BLUE = "\033[34m"
    RED = "\033[31m"
    INVERT = "\033[7m"

    @staticmethod
    def launch(filename: str = None):
        """Launches the full-featured Aqua sovereign interactive editor."""
        lines = [""]
        if filename and os.path.exists(filename):
            with open(filename, "r") as f:
                lines = f.read().splitlines() or [""]

        cur_x = 0
        cur_y = 0
        status_msg = " AQUA Editor v1.0 | Press Ctrl+S to Save, Ctrl+Q to Quit, Ctrl+R to Run Science Core "
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        def render_screen():
            # Clear screen & home cursor
            sys.stdout.write("\033[2J\033[H")
            rows, cols = os.get_terminal_size()
            
            # Header Bar
            header = f"{AquaTerminalEditor.INVERT}{AquaTerminalEditor.CYAN}  ❖ AQUAMARINE SOVEREIGN SCIENTIFIC EDITOR ❖  {filename or '[New Buffer]':<30}{AquaTerminalEditor.RESET}\n"
            sys.stdout.write(header)

            # File Content
            max_view_rows = rows - 3
            for i in range(max_view_rows):
                if i < len(lines):
                    line_content = lines[i][:cols - 6]
                    # Simple syntax color for math symbols
                    colored_line = line_content.replace("=", f"{AquaTerminalEditor.YELLOW}={AquaTerminalEditor.RESET}")
                    line_str = f"{AquaTerminalEditor.MAGENTA}{i+1:3d} │{AquaTerminalEditor.RESET} {colored_line}"
                    sys.stdout.write(line_str + "\n")
                else:
                    sys.stdout.write(f"{AquaTerminalEditor.MAGENTA}  ~ │{AquaTerminalEditor.RESET}\n")

            # Status Bar at bottom
            status_bar = f"\033[{rows-1};1H{AquaTerminalEditor.INVERT}{AquaTerminalEditor.GREEN}{status_msg:<{cols}}{AquaTerminalEditor.RESET}"
            sys.stdout.write(status_bar)

            # Move cursor to active position
            sys.stdout.write(f"\033[{cur_y + 2};{cur_x + 7}H")
            sys.stdout.flush()

        try:
            tty.setraw(fd)
            while True:
                render_screen()
                ch = sys.stdin.read(1)

                # Ctrl+Q: Quit
                if ch == '\x11':
                    break

                # Ctrl+S: Save File
                elif ch == '\x13':
                    save_path = filename or "output.aqua"
                    with open(save_path, "w") as f:
                        f.write("\n".join(lines))
                    status_msg = f" [SAVED] Successfully written to {save_path} "

                # Ctrl+R: Execute Pure Symbolic CAS on current line
                elif ch == '\x12':
                    current_expr = lines[cur_y].strip()
                    try:
                        # Quick limit evaluation test
                        res = AdvancedSymbolicCAS.evaluate_symbolic_limit_lhopital("1-cos(x)", "x^2", 0.0, "x")
                        status_msg = f" [CAS RESULT] Limit (1-cos(x))/x^2 = {res['exact_limit_value']} "
                    except Exception as e:
                        status_msg = f" [CAS ERROR] {str(e)[:30]} "

                # Enter key
                elif ch in ('\r', '\n'):
                    rest = lines[cur_y][cur_x:]
                    lines[cur_y] = lines[cur_y][:cur_x]
                    lines.insert(cur_y + 1, rest)
                    cur_y += 1
                    cur_x = 0

                # Backspace / Delete
                elif ch in ('\x7f', '\x08'):
                    if cur_x > 0:
                        lines[cur_y] = lines[cur_y][:cur_x-1] + lines[cur_y][cur_x:]
                        cur_x -= 1
                    elif cur_y > 0:
                        prev_len = len(lines[cur_y - 1])
                        lines[cur_y - 1] += lines[cur_y]
                        lines.pop(cur_y)
                        cur_y -= 1
                        cur_x = prev_len

                # Escape sequences (Arrow keys)
                elif ch == '\x1b':
                    seq = sys.stdin.read(2)
                    if seq == '[A':  # Up
                        if cur_y > 0:
                            cur_y -= 1
                            cur_x = min(cur_x, len(lines[cur_y]))
                    elif seq == '[B':  # Down
                        if cur_y < len(lines) - 1:
                            cur_y += 1
                            cur_x = min(cur_x, len(lines[cur_y]))
                    elif seq == '[C':  # Right
                        if cur_x < len(lines[cur_y]):
                            cur_x += 1
                    elif seq == '[D':  # Left
                        if cur_x > 0:
                            cur_x -= 1

                # Printable ASCII characters
                elif 32 <= ord(ch) <= 126:
                    lines[cur_y] = lines[cur_y][:cur_x] + ch + lines[cur_y][cur_x:]
                    cur_x += 1

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            sys.stdout.write("\033[2J\033[H")
            sys.stdout.flush()

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    AquaTerminalEditor.launch(target)
