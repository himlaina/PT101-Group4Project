def SRTF():
    processes = int(input("Enter the number of processes: "))

    processID = []
    AT = []
    BT = []

    for i in range(processes):
        print("\nProcess", i + 1)
        processID.append("P" + str(i + 1))

        arrival_time = int(input("Arrival Time: "))
        while arrival_time < 0:
            arrival_time = int(input("Cannot be negative, try again: "))
        AT.append(arrival_time)

        burst_time = int(input("Burst Time: "))
        while burst_time <= 0:
            burst_time = int(input("Must be more than 0, try again: "))
        BT.append(burst_time)

    def gantt_chart(blocks):
        merged = []
        for block in blocks:
            if len(merged) > 0 and merged[-1][0] == block[0] and merged[-1][2] == block[1]:
                merged[-1][2] = block[2]
            else:
                merged.append([block[0], block[1], block[2]])

        line1 = "|"
        line2 = str(merged[0][1])
        for block in merged:
            line1 += " " + block[0] + " |"
            line2 = line2.ljust(len(line1) - 1) + str(block[2])
        print("Gantt Chart:")
        print(line1)
        print(line2)

    def results(name, blocks, CT, start):
        print("\n" + name.center(50))
        gantt_chart(blocks)

        print("\nPID\tAT\tBT\tCT\tTAT\tWT\tRT")
        total_TAT = 0
        total_WT = 0
        total_RT = 0
        for i in range(processes):
            TAT = CT[i] - AT[i]
            WT = TAT - BT[i]
            RT = start[i] - AT[i]
            total_TAT += TAT
            total_WT += WT
            total_RT += RT
            print(processID[i], AT[i], BT[i], CT[i], TAT, WT, RT, sep="\t")

        print("\nAverage TAT: ", round(total_TAT / processes, 2))
        print("Average WT: ", round(total_WT / processes, 2))
        print("Average RT: ", round(total_RT / processes, 2))
        print("\n")

    CT = [0] * processes
    start = [-1] * processes
    remaining = BT.copy()
    blocks = []
    time = 0
    done = 0

    while done < processes:
        pick = -1
        for i in range(processes):
            if AT[i] <= time and remaining[i] > 0:
                if pick == -1 or remaining[i] < remaining[pick]:
                    pick = i
                elif remaining[i] == remaining[pick] and AT[i] < AT[pick]:
                    pick = i

        if pick == -1:
            blocks.append(["Idle", time, time + 1])
            time += 1
        else:
            if start[pick] == -1:
                start[pick] = time
            remaining[pick] -= 1
            blocks.append([processID[pick], time, time + 1])
            time += 1
            if remaining[pick] == 0:
                CT[pick] = time
                done += 1

    results("Shortest Remaining Time First", blocks, CT, start)


if __name__ == "__main__":
    SRTF()