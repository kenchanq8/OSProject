
from scheduler import *


print("1-Preemptive priority(PP)\n"
             "2-Round Robin(RR)\n"
             "3-Shortest Remaining Time First(SRTF)\n"
             "4-Multi-level feedback queue Custom algorithm(Mlf)\n")

choose=int(input("Select scheduling :\n"))

'''
process_srtf = [Process(1, 0, 8, 0),
                    Process(2, 1, 4, 0),
                    Process(3, 2, 9, 0),
                    Process(4, 3, 5, 0)]

process_rr_pp = [Process(1, 0, 5, 4),
              Process(2, 0, 3, 1),
              Process(3, 1, 1, 2),
              Process(4, 3, 2, 3),
              Process(5, 5, 3, 1)]
              '''
S = Scheduler()
S.read_file('test')
S.printTasks()




while choose!=0:
    if choose==1:
        S.pp()

    elif choose ==2:
        S.rr()

    elif choose ==3:
        S.srtf()

    elif choose==4:

        S.mlfq()
    else:
        print("AGIAN!")

    print("1-Preemptive priority(PP)\n"
          "2-Round Robin(RR)\n"
          "3-Shortest Remaining Time First(SRTF)\n"
          "4-Multi-level feedback queue Custom algorithm(Mlf)\n")

    choose = int(input("Select scheduling :\n"))

print("Thank You")

