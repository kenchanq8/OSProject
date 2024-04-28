# import time
from process import *


def avg_rt(finished_process):
    # caculate average response time
    total_rt = 0
    for process in finished_process:
        process_rt = process.first_started - process.at     # rt formula
        process.rt = process_rt         # record rt of process
        total_rt += process_rt          # calc total
    return total_rt/len(finished_process)   # return average


def avg_tat(finished_process):
    total_tat = 0
    for process in finished_process:
        process_tat = process.ft - process.at  # tat formula
        total_tat += process_tat    # calc total
        process.tat = process_tat   # recording tat of process
    return total_tat / len(finished_process)   # return average


def avg_wt(finished_process):
    total_wt = 0
    for process in finished_process:
        process_wt = process.tat - process.bt  # wt formula
        total_wt += process_wt      # calc total
        process.wt = process_wt     # recording wt of process
    return total_wt / len(finished_process)   # return average


class Scheduler:
    def __init__(self, process):
        self.process = process
        self.finished_process = []
        self.current_process = None
        self.arrived_process = []   # ---might cause logic error later---

    # DONE (just add more comments)
    def pp(self):
        # preemptive priority
        if not self.process:  # leave if empty
            return

        current_time = 0

        while self.process:
            arrived_process = []

            print("time:", current_time, "\n")

            if self.process:  # check if list is not empty
                print("arrived processes:")

                # sort processes based on arrival time then priority
                sorted_process = []
                for process in self.process:
                    insert = False
                    for i in range(len(sorted_process)):
                        if process.at < sorted_process[i].at or (process.at == sorted_process[i].at and process.priority
                        < sorted_process[i].priority):
                            sorted_process.insert(i, process)
                            insert = True
                            break
                    if not insert:
                        sorted_process.append(process)
                for process in sorted_process:
                    # filter processes based on arrival time
                    if process.at <= current_time:
                        arrived_process.append(process)
                        print(f"p{process.pid}: ({process.remaining_time}, {process.priority})", sep='')
            else:
                print("No processes in the list")

            print(" ")

            if not arrived_process:
                # if no processes arrived
                next_arrival = min(process.at for process in self.process)
                current_time = next_arrival
                continue

            Hpriority_process = None
            h_priority = float('inf')  # infinity

            # choose the highest priority process
            for process in arrived_process:
                if process.priority < h_priority:
                    Hpriority_process = process
                    h_priority = process.priority
                    if Hpriority_process.remaining_time == Hpriority_process.bt:
                        Hpriority_process.first_started = current_time

            print("running process: p", Hpriority_process.pid, sep='')
            print("____________________")

            current_time += 1  # increment time
            Hpriority_process.remaining_time -= 1  # decrement process time

            if Hpriority_process.remaining_time == 0:
                # process complete
                Hpriority_process.ft = current_time  # store finish time
                self.finished_process.append(Hpriority_process)  # add to finished processes
                arrived_process.remove(Hpriority_process)  # remove from arrival list
                self.process.remove(Hpriority_process)  # Remove from process list

        print("time:", current_time, "\n")
        print("Running finished\n")

        print("average response time: ", avg_rt(self.finished_process))
        print("average turn around time time: ", avg_tat(self.finished_process))
        print("average waiting time: ", avg_wt(self.finished_process))

    # DONE (just remove testing comments)
    def rr(self, quantum):
        # round robin

        if not self.process:    # empty list
            return False

        current_time = 0    # start timer
        current_process_qtimer = quantum    # set timer for current running process

        while self.process or self.arrived_process:
            print("time:", current_time, "\n")
            if self.process:    # check if list is not empty
                for process in self.process:    # loop over all process
                    # print(f"p{process.pid} checking") --testing-- REMOVE LATER!!!!!!!!!!
                    if process.at <= current_time:
                        self.arrived_process.append(process)    # add process to arrived process list
                        # print(f"p{process.pid} added") --testing-- REMOVE LATER!!!!!!!!!!
                        self.process = self.process[1:]    # remove process from process list
                        # --testing REMOVE LATER!!!!!!!!!!
                        # for p in self.process:
                        #     print(f"p{p.pid} exists")
                # print(" ")

            if self.arrived_process:
                # print all arrived processes with their remaining time
                print("arrived processes:")
                for process in self.arrived_process:
                    print(f"p{process.pid}: {process.remaining_time}", sep='')

                print(" ")

                # set current running process to the first arrived process
                self.current_process = self.arrived_process[0]

                if self.current_process.remaining_time > 0:
                    if current_process_qtimer > 0:
                        print("running process: p", self.current_process.pid, sep='')
                        print("____________________")
                        if self.current_process.remaining_time == self.current_process.bt:
                            self.current_process.first_started = current_time
                        current_process_qtimer -= 1    # decrement quantum timer for process
                        self.current_process.remaining_time -= 1    # decrement remaining time for process

                        if self.current_process.remaining_time == 0:    # check if process finished
                            self.finished_process.append(self.current_process)  # add process to finished list
                            self.arrived_process = self.arrived_process[1:]     # remove current and push elems
                            self.current_process.ft = current_time + 1  # record finish time
                            current_process_qtimer = quantum

                        if current_process_qtimer == 0:     # got switched without finishing
                            self.arrived_process = self.arrived_process[1:]     # remove first element

                            # add process arriving next iteration before the currently switched process
                            for process in self.process:
                                if process.at == (current_time + 1):    # if next process arrives next iteration
                                    self.arrived_process.append(process)  # add process to arrived process list
                                    self.process.remove(process)  # remove process from process list
                                    # (avoids repetition in the arrived process list)

                            self.arrived_process.append(self.current_process)   # readd switched process
                            current_process_qtimer = quantum   # reset quantum timer

                current_time += 1   # increment timer

            else:   # no processes passed
                print("No processes arrived")

        print("\nrunning finished at time", current_time)   # end of running queue

        # --testing-- REMOVE LATER!!!!!!!!!!!!!
        # for p in self.finished_process:
        #     print(f"p{p.pid}, ft {p.ft}, first started {p.first_started}")

        # calculate averages
        print("\naverage response time: ", avg_rt(self.finished_process))
        print("average turn around time time: ", avg_tat(self.finished_process))
        print("average waiting time: ", avg_wt(self.finished_process))

    # DONE
    def srtf(self):
        # shortest remaining time first

        if not self.process:  # empty process passed
            return False

        current_time = 0  # start timer

        while self.process or self.arrived_process:
            print("time:", current_time, "\n")
            if self.process:  # check if list is not empty
                for process in self.process:
                    # filter processes based on arrival time
                    if process.at <= current_time:
                        self.arrived_process.append(process)    # add to arrived processes
                        self.process = self.process[1:]     # remove from process list

            if self.arrived_process:    # check if there are arrived processes
                # print all arrived processes with their remaining time
                print("arrived processes:")

                # print arrived processes
                for process in self.arrived_process:
                    print(f"p{process.pid}: {process.remaining_time}", sep='')

                # sort arrived processes based on remaining time
                for i in range(len(self.arrived_process)):
                    min_i = i
                    for j in range(i+1, len(self.arrived_process)):
                        if self.arrived_process[j].remaining_time < self.arrived_process[min_i].remaining_time:
                            min_i = j
                        self.arrived_process[min_i], self.arrived_process[i] = self.arrived_process[i], self.arrived_process[min_i]
                print(" ")

                shortest_process = self.arrived_process[0]  # chooses the shortest process

                # record process first started time
                if shortest_process.remaining_time == shortest_process.bt:
                    shortest_process.first_started = current_time

                # print running process
                print("running process: p", shortest_process.pid, sep='')
                print("____________________")

                current_time += 1  # increment time
                shortest_process.remaining_time -= 1  # decrement process remaining time

                # procees complete
                if shortest_process.remaining_time == 0:
                    shortest_process.ft = current_time  # store finish time
                    self.finished_process.append(shortest_process)  # add to finished processes
                    self.arrived_process = self.arrived_process[1:]  # remove from arrival list

            else:   # no arrived processes
                current_time += 1   # increment time

        print("running finished at time", current_time)   # end of running queue

        # calculate averages
        print("\naverage response time: ", avg_rt(self.finished_process))
        print("average turn around time time: ", avg_tat(self.finished_process))
        print("average waiting time: ", avg_wt(self.finished_process))

    def mlfq(self):
        # custom algorithm
        pass


def read_file(file):
    # read input file and create list
    pass


def random_file(file):
    # generate random file
    pass


process1 = [Process(1, 0, 5, 4),
           Process(2, 0, 3, 1),
           Process(3, 1, 1, 2),
           Process(4, 3, 2, 3),
           Process(5, 5, 3, 3)]

process2 = [Process(1, 0, 8, 0),
            Process(2, 1, 4, 0),
            Process(3, 2, 9, 0),
            Process(4, 3, 5, 0)]

process3 = []

# scheduler = Scheduler(process1)
scheduler = Scheduler(process2)
# scheduler = Scheduler(process3)
scheduler.srtf()
# scheduler.pp()
# scheduler.rr(quantum=2)



# print(finish_time)
