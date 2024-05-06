from scheduler import *

# create scheduler
S = Scheduler()
S.read_file('test')

while True:
    # Show menu
    print("1-Preemptive priority (PP)\n"
          "2-Round Robin (RR)\n"
          "3-Shortest Remaining Time First (SRTF)\n"
          "4-Multi-level feedback queue Custom algorithm (MLFQ)\n")
    # take selection
    choice = int(input("Select scheduling: "))
    print("____________________")

    if choice == 0:     # Exit
        break

    elif choice == 1:   # PP
        print("Running Preemptive Priority\n")
        S.pp()

    elif choice == 2:   # RR
        print("Running Round Robin\n")
        S.rr()

    elif choice == 3:   # SRTF
        print("Running Shortest Remaining Time First\n")
        S.srtf()

    elif choice == 4:   # MLFQ
        print("Running Multi-Level Feedback Queue\n")
        S.mlfq()
    else:               # Wrong selection
        print("AGIAN!\n")

print("Thank You")

