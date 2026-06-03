import subprocess
import sys

packages = [
    "matplotlib",
    "aiohttp",
    "traci",
    "pandas",
    "numpy",
    "scikit-learn",
    "sumolib",
    "seaborn"
]

for package in packages:
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print(f"[OK] {package} installed")