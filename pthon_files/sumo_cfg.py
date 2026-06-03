import os
import traci


SUMO_EXE = r"C:\sumo-win64-1.23.1\sumo-1.23.1\bin\sumo-gui.exe"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = os.path.dirname(CURRENT_DIR)

SUMO_CONFIG = os.path.join(PROJECT_DIR, "mySimulation.sumocfg")


# ============================================================
# START SUMO
# ============================================================

def start_sumo():
    if not os.path.exists(SUMO_CONFIG):
        raise FileNotFoundError(f"Config not found: {SUMO_CONFIG}")

    if not os.path.exists(SUMO_EXE):
        raise FileNotFoundError(f"SUMO not found: {SUMO_EXE}")

    traci.start([
        SUMO_EXE,
        "-c",
        SUMO_CONFIG,
        "--start"
    ])

    return True