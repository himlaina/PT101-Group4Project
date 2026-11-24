def non_preemptive_sjf():
    print("=== NON-PREEMPTIVE SHORTEST JOB FIRST (SJF) SCHEDULING ===\n")
    
    try:
        n = int(input("Enter number of processes: "))
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return

    processes = []
    for i in range(n):
        print(f"\n--- Process {i + 1} ---")
        pid = input("Enter Process ID (e.g., P1): ").strip()
        at = int(input(f"Enter Arrival Time for {pid}: "))
        bt = int(input(f"Enter Burst Time for {pid}: "))
        processes.append({
            "pid": pid,
            "at": at,
            "bt": bt,
            "ct": 0,
            "tat": 0,
            "wt": 0,
            "rt": 0,
            "completed": False
        })

    current_time = 0
    completed_count = 0
    timeline = []  

    while completed_count < n:
        ready_queue = [p for p in processes if p["at"] <= current_time and not p["completed"]]

        if not ready_queue:
            next_arrival = min(p["at"] for p in processes if not p["completed"])
            timeline.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            continue

        selected = min(ready_queue, key=lambda p: (p["bt"], p["at"]))

        start_time = current_time
        end_time = start_time + selected["bt"]

        selected["ct"] = end_time
        selected["tat"] = selected["ct"] - selected["at"]
        selected["wt"] = selected["tat"] - selected["bt"]
        selected["rt"] = start_time - selected["at"]  # In non-preemptive SJF, RT == WT
        selected["completed"] = True

        timeline.append((selected["pid"], start_time, end_time))
        current_time = end_time
        completed_count += 1

    print("\n" + "=" * 60)
    print("GANTT CHART / EXECUTION TIMELINE")
    print("=" * 60)
    
    bar = "|"
    time_markers = f"{timeline[0][1]}"
    for pid, start, end in timeline:
        segment = f"  {pid}  |"
        bar += segment
        time_markers += f"{end:>{len(segment)}}"
    
    print(bar)
    print(time_markers)

    print("\nStep-by-Step Timeline:")
    for pid, start, end in timeline:
        print(f"  [{start} -> {end}] : {pid}")

    print("\n" + "=" * 60)
    print("PER-PROCESS METRICS")
    print("=" * 60)
    header = f"{'PID':<8}{'AT':<8}{'BT':<8}{'CT':<8}{'TAT':<8}{'WT':<8}{'RT':<8}"
    print(header)
    print("-" * len(header))

    total_tat = 0
    total_wt = 0
    total_rt = 0

    for p in processes:
        print(f"{p['pid']:<8}{p['at']:<8}{p['bt']:<8}{p['ct']:<8}{p['tat']:<8}{p['wt']:<8}{p['rt']:<8}")
        total_tat += p["tat"]
        total_wt += p["wt"]
        total_rt += p["rt"]

    avg_tat = total_tat / n
    avg_wt = total_wt / n
    avg_rt = total_rt / n

    print("\n" + "=" * 60)
    print("AVERAGE METRICS")
    print("=" * 60)
    print(f"Average Turnaround Time (TAT) : {avg_tat:.2f}")
    print(f"Average Waiting Time (WT)     : {avg_wt:.2f}")
    print(f"Average Response Time (RT)    : {avg_rt:.2f}")
    print("=" * 60)


if __name__ == "__main__":
    non_preemptive_sjf()
