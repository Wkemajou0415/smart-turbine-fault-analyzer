#Setup
import time
from collections import Counter
import matplotlib.pyplot as plt
import csv

records = []

turbine_data = [
    {"current": 95, "temperature": 45, "vibration": 2},
    {"current": 130, "temperature": 70, "vibration": 6},
    {"current": 110, "temperature": 55, "vibration": 3}
]

fault_counts = {
    "Overcurrent": 0,
    "Overheating": 0,
    "High Vibration": 0,
    "Sensor Failure": 0,
    "Emergency Shutdown": 0
}

critical_faults = 0

for record in turbine_data:

    current = record["current"]
    temp = record["temperature"]
    vibration = record["vibration"]

    status = "Normal"
    fault = "None"

    if current > 120:
        status = "Warning"
        fault = "Overcurrent"
        fault_counts["Overcurrent"] += 1

    if temp > 60:
        status = "Warning"
        fault = "Overheating"
        fault_counts["Overheating"] += 1

    if vibration > 5:
        status = "Warning"
        fault = "High Vibration"
        fault_counts["High Vibration"] += 1

    if temp > 60 and vibration > 5:
        status = "Critical Fault"
        fault = "Overheat + Vibration"

        critical_faults += 1

    time.sleep(1)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    print(f"{timestamp} | Current:{current}A | Temp:{temp}°C | "
      f"Vibration:{vibration} | Status:{status} | Fault:{fault}")
    
    records.append({
    "timestamp": timestamp,
    "current": current,
    "temperature": temp,
    "vibration": vibration,
    "status": status,
    "fault": fault
})

    if critical_faults >= 3:
        print("\nEMERGENCY SHUTDOWN")
        fault_counts["Emergency Shutdown"] += 1
        break

# Graph
timestamps = [r["timestamp"] for r in records]
currents = [r["current"] for r in records]
temperatures = [r["temperature"] for r in records]
vibrations = [r["vibration"] for r in records]
statuses = [r["status"] for r in records]

# Graph for current

plt.figure(figsize=(10, 5))

plt.plot(timestamps, currents, marker="o", label="Current")

critical_added = False

for i, status in enumerate(statuses):
    if status == "Critical Fault":
        if not critical_added:
            plt.scatter(timestamps[i], currents[i], s=120, label="Critical Fault")
            critical_added = True
        else:
            plt.scatter(timestamps[i], currents[i], s=120)

plt.xlabel("Time")
plt.ylabel("Current (A)")
plt.title("Current Trend with Critical Faults")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig("current_fault_graph.png", dpi=300)
plt.show()

# Graph for temperature

plt.figure(figsize=(10, 5))

plt.plot(timestamps, temperatures, marker="o", label="Temperature")

critical_added = False

for i, status in enumerate(statuses):
    if status == "Critical Fault":
        if not critical_added:
            plt.scatter(timestamps[i], temperatures[i], s=120, label="Critical Fault")
            critical_added = True
        else:
            plt.scatter(timestamps[i], temperatures[i], s=120)

plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.title("Temperature Trend with Critical Faults")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig("temp_fault_graph.png", dpi=300)
plt.show()

# Graph for vibration

plt.figure(figsize=(10, 5))

plt.plot(timestamps, vibrations, marker="o", label="Vibration")

critical_added = False

for i, status in enumerate(statuses):
    if status == "Critical Fault":
        if not critical_added:
            plt.scatter(timestamps[i], vibrations[i], s=120, label="Critical Fault")
            critical_added = True
        else:
            plt.scatter(timestamps[i], vibrations[i], s=120)

plt.xlabel("Time")
plt.ylabel("Vibration")
plt.title("Vibration Trend with Critical Faults")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.savefig("vib_fault_graph.png", dpi=300)
plt.show()

# Maintenance Report

total_events = len(records)

normal_events = sum(1 for r in records if r["status"] == "Normal")
warning_events = sum(1 for r in records if r["status"] == "Warning")
critical_events = sum(1 for r in records if r["status"] == "Critical Fault")

if sum(fault_counts.values()) > 0:
    most_common_fault = max(fault_counts, key=fault_counts.get)
else:
    most_common_fault = "None"

print("\n=== MAINTENANCE REPORT ===")
print(f"Total Events: {total_events}")
print(f"Normal Events: {normal_events}")
print(f"Warning Events: {warning_events}")
print(f"Critical Faults: {critical_events}")

print("\n--- Fault Summary ---")
for fault, count in fault_counts.items():
    print(f"{fault}: {count}")

print(f"\nMost Common Fault: {most_common_fault}")

# Save Fault Logs

filename = "fault_logs.csv"

with open(filename, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Timestamp",
        "Current",
        "Temperature",
        "Vibration",
        "Status",
        "Fault"
    ])

    for r in records:
        writer.writerow([
            r["timestamp"],
            r["current"],
            r["temperature"],
            r["vibration"],
            r["status"],
            r["fault"]
        ])

print(f"\nFault logs saved to {filename}")