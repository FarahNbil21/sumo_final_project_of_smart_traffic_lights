import sys
import traci
import csv
import os
from sumo_cfg import start_sumo,SUMO_CONFIG,SUMO_EXE

project_root = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(project_root)
for p in [project_root, parent_dir]:
    if p not in sys.path:
        sys.path.append(p)

# ============================================
# SUMO CONFIG
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
# GET ALL TRAFFIC LIGHTS
# ============================================

traffic_lights = traci.trafficlight.getIDList()

print("Traffic Lights Found:")
print(traffic_lights)

# ============================================
# CREATE CSV FILE
# ============================================

csv_file = open("traffic_data.csv", "w", newline="")

writer = csv.writer(csv_file)

writer.writerow([
    "Step",
    "Intersection",
    "Total Cars",
    "Waiting Cars",
    "Average Speed",
    "Waiting Time"
])

# ============================================
# MAIN LOOP
# ============================================

while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()

    current_step = traci.simulation.getTime()

    print("\n==============================")
    print(f"Simulation Step: {current_step}")

    for tl in traffic_lights:

        lanes = traci.trafficlight.getControlledLanes(tl)

        total_cars = 0
        waiting_cars = 0
        total_speed = 0
        total_waiting_time = 0

        unique_lanes = set(lanes)

        for lane in unique_lanes:

            # عدد العربيات
            vehicle_count = traci.lane.getLastStepVehicleNumber(lane)

            # العربيات الواقفة
            halting_count = traci.lane.getLastStepHaltingNumber(lane)

            # متوسط السرعة
            mean_speed = traci.lane.getLastStepMeanSpeed(lane)

            # وقت الانتظار
            waiting_time = traci.lane.getWaitingTime(lane)

            total_cars += vehicle_count
            waiting_cars += halting_count
            total_speed += mean_speed
            total_waiting_time += waiting_time

        # حساب متوسط السرعة
        avg_speed = 0

        if len(unique_lanes) > 0:
            avg_speed = total_speed / len(unique_lanes)

        # ============================================
        # PRINT RESULTS
        # ============================================

        print(f"\nIntersection: {tl}")

        print(f"Total Cars: {total_cars}")

        print(f"Waiting Cars: {waiting_cars}")

        print(f"Average Speed: {avg_speed:.2f}")

        print(f"Waiting Time: {total_waiting_time:.2f}")

        # ============================================
        # SAVE TO CSV
        # ============================================

        writer.writerow([
            current_step,
            tl,
            total_cars,
            waiting_cars,
            round(avg_speed, 2),
            round(total_waiting_time, 2)
        ])

# ============================================
# CLOSE EVERYTHING
# ============================================

csv_file.close()

traci.close()

print("\nSimulation Finished")
print("Traffic data saved to traffic_data.csv")