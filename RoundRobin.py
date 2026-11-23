
from collections import deque


def read_int(prompt, minimum=0):
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                print(f"Please enter a value greater than or equal to {minimum}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_processes():
    count = read_int("Enter number of processes: ", 1)
    processes = []
    used_ids = set()

    for i in range(count):
        print(f"\nProcess {i + 1}")

        while True:
            pid = input("Process ID (e.g., P1): ").strip()

            if not pid:
                print("Process ID cannot be empty.")
            elif pid in used_ids:
                print("Process ID must be unique.")
            else:
                used_ids.add(pid)
                break

        arrival = read_int("Arrival Time: ", 0)
        burst = read_int("Burst Time: ", 1)

        processes.append({
            "pid": pid,
            "arrival": arrival,
            "burst": burst
        })

    return processes


def round_robin(processes, quantum):

    info = {
        p["pid"]: {
            "arrival": p["arrival"],
            "burst": p["burst"],
            "remaining": p["burst"],
            "first_start": None,
            "completion": None
        }
        for p in processes
    }

    arrival_order = sorted(
        processes,
        key=lambda p: p["arrival"]
    )

    ready = deque()
    timeline = []
    current_time = 0
    next_process = 0
    completed = 0
    total = len(processes)

    while completed < total:

        if not ready:

            if (next_process < total and
                    current_time < arrival_order[next_process]["arrival"]):
                current_time = arrival_order[next_process]["arrival"]

            while (next_process < total and
                   arrival_order[next_process]["arrival"] <= current_time):

                ready.append(arrival_order[next_process]["pid"])
                next_process += 1

        pid = ready.popleft()
        item = info[pid]

        if item["first_start"] is None:
            item["first_start"] = current_time

        start_time = current_time
        run_time = min(quantum, item["remaining"])

        current_time += run_time
        item["remaining"] -= run_time

        while (next_process < total and
               arrival_order[next_process]["arrival"] <= current_time):

            ready.append(arrival_order[next_process]["pid"])
            next_process += 1

        timeline.append((
            pid,
            start_time,
            current_time,
            item["remaining"]
        ))

        if item["remaining"] > 0:
            ready.append(pid)
        else:
            item["completion"] = current_time
            completed += 1

    metrics = []

    for p in processes:
        item = info[p["pid"]]

        ct = item["completion"]
        tat = ct - item["arrival"]
        wt = tat - item["burst"]
        rt = item["first_start"] - item["arrival"]

        metrics.append({
            "pid": p["pid"],
            "at": item["arrival"],
            "bt": item["burst"],
            "ct": ct,
            "tat": tat,
            "wt": wt,
            "rt": rt
        })

    return timeline, metrics


def display_results(timeline, metrics, quantum):

    print("\n" + "=" * 68)
    print("          ROUND ROBIN CPU SCHEDULING RESULTS")
    print("=" * 68)

    print(f"Time Quantum: {quantum}")

    print("\nGANTT CHART / EXECUTION TIMELINE")

    print(" | ".join(
        f"{pid} ({start}-{end})"
        for pid, start, end, _ in timeline
    ))

    print("Time points:", " -> ".join(
        [str(timeline[0][1])] +
        [str(item[2]) for item in timeline]
    ))

    print("\nQUANTUM-BY-QUANTUM TRACE")

    print(
        f"{'Step':<6}{'Process':<12}"
        f"{'Start':<10}{'End':<10}{'Remaining BT':<15}"
    )

    print("-" * 53)

    for step, (pid, start, end, remaining) in enumerate(
        timeline, start=1
    ):
        print(
            f"{step:<6}{pid:<12}{start:<10}"
            f"{end:<10}{remaining:<15}"
        )

    print("\nPROCESS PERFORMANCE TABLE")

    print(
        f"{'PID':<10}{'AT':<8}{'BT':<8}"
        f"{'CT':<8}{'TAT':<8}{'WT':<8}{'RT':<8}"
    )

    print("-" * 58)

    for row in metrics:
        print(
            f"{row['pid']:<10}{row['at']:<8}"
            f"{row['bt']:<8}{row['ct']:<8}"
            f"{row['tat']:<8}{row['wt']:<8}"
            f"{row['rt']:<8}"
        )

    count = len(metrics)

    avg_tat = sum(r["tat"] for r in metrics) / count
    avg_wt = sum(r["wt"] for r in metrics) / count
    avg_rt = sum(r["rt"] for r in metrics) / count

    print("\nAVERAGE METRICS")

    print(f"Average Turnaround Time: {avg_tat:.2f}")
    print(f"Average Waiting Time: {avg_wt:.2f}")
    print(f"Average Response Time: {avg_rt:.2f}")

    print("=" * 68)


def main():

    print("=" * 68)
    print("       ROUND ROBIN CPU SCHEDULING SIMULATOR")
    print("                  PT 101 - Topic 2")
    print("=" * 68)

    processes = get_processes()

    quantum = read_int("\nEnter Time Quantum: ", 1)

    timeline, metrics = round_robin(processes, quantum)

    display_results(timeline, metrics, quantum)


if __name__ == "__main__":
    main()
