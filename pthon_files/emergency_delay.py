import traci
import os
import sys
from sumo_cfg import start_sumo,SUMO_CONFIG,SUMO_EXE

project_root = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(project_root)
for p in [project_root, parent_dir]:
    if p not in sys.path:
        sys.path.append(p)

# ============================================
# START SUMO
# ============================================
sumo_running = False
traffic_nodes = {}
tl_info = {}

if not os.path.exists(SUMO_CONFIG):
    print(f"  Config not found: {SUMO_CONFIG}")
elif not os.path.exists(SUMO_EXE):
    print(f"  SUMO not found: {SUMO_EXE}")
else:
    try:
        start_sumo()

        print("  SUMO running!")
        sumo_running = True
    except Exception as e:
        print(e)
# ============================================
# EMERGENCY VEHICLE SETTINGS
# ============================================

# اسم عربية الإسعاف
EMERGENCY_ID = "t_0"

# متغيرات الحساب
start_time = None
end_time = None

# ============================================
# MAIN LOOP
# ============================================

while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()

    current_time = traci.simulation.getTime()

    # كل العربيات الموجودة حاليًا
    vehicles = traci.vehicle.getIDList()

    # ============================================
    # DETECT AMBULANCE
    # ============================================

    if EMERGENCY_ID in vehicles:

        # أول ظهور للإسعاف
        if start_time is None:
            start_time = current_time

            print("\n===================================")
            print(f" Ambulance detected at time: {start_time}")

        # بيانات الإسعاف
        speed = traci.vehicle.getSpeed(EMERGENCY_ID)

        road = traci.vehicle.getRoadID(EMERGENCY_ID)

        waiting_time = traci.vehicle.getWaitingTime(EMERGENCY_ID)

        print("\n-----------------------------------")
        print(f"Time: {current_time}")
        print(f"Current Road: {road}")
        print(f"Speed: {speed:.2f} m/s")
        print(f"Waiting Time: {waiting_time:.2f} sec")

    # ============================================
    # CHECK IF AMBULANCE ARRIVED
    # ============================================

    elif start_time is not None and end_time is None:

        end_time = current_time

        total_trip_time = end_time - start_time

        print("\n===================================")
        print(" Ambulance reached destination!")

        print(f"Start Time: {start_time}")
        print(f"Arrival Time: {end_time}")

        print(f"Total Delay / Travel Time: {total_trip_time:.2f} sec")

        break


# ============================================
# CLOSE SUMO
# ============================================

traci.close()

print("\nSimulation Finished")