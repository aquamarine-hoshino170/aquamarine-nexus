import subprocess
import sys

def auto_sync(ver="2.4.0"):
    print(f"\n[*] Synchronizing entire scientific ecosystem (v{ver})...")
    subprocess.run(["sed", "-i", f's/version = ".*"/version = "{ver}"/g', "pyproject.toml"])
    subprocess.run(["sed", "-i", f's/version=".*"/version="{ver}"/g', "setup.py"])
    subprocess.run([sys.executable, "-m", "pip", "install", "-e", ".", "--no-deps"], check=True)
    print("\n[+] System is fully automated and synchronized!\n")

if __name__ == "__main__":
    v = sys.argv[1] if len(sys.argv) > 1 else "2.4.0"
    auto_sync(v)
