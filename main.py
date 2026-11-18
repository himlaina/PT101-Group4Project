from SRTF import SRTF

# Program Header
while True:
    print("=" * 50 + "\n")
    print("Group 4 CPU Scheduling Simulation".center(50) + "\n")
    print("=" * 50 + "\n")
    print("[1] First Come First Serve (FCFS)")
    print("[2] Shortest Job First (SJF)")
    print("[3] Shortest Remaining Time First (SRTF)")
    print("[4] Round Robin (RR)")
    print("[5] Comparison")
    print("[6] Exit")
    choice = int(input("\nEnter your choice: "))
    print("\n" + "=" * 50 + "\n")
    
    if choice == 1:
        FCFS()
        
    elif choice == 2:
        SFJ()
        
    elif choice == 3:
        print("Shortest Remaining Time First Algorithm" .center(50), "\n")
        SRTF()
        
    elif choice == 4:
        RoundRobin()
        
    elif choice == 5:
        Comparison()
        
    elif choice == 6:
        print("Exiting the program.")
        break   
    
    else:
        print("Invalid choice. Please enter a number between 1 and 5.\n")