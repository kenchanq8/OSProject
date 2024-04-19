# import time
from process import *


def avg_rt(finished_process):
    # caculate average response time
    total_rt = 0
    for process in finished_process:
        process_rt = process.first_started - process.at     # rt formula
        process.rt = process_rt
        total_rt += process_rt
    return total_rt/len(finished_process)


def avg_tat(finished_process):
    total_tat = 0
    for process in finished_process:
        process_tat = process.ft - process.at  # tat formula
        total_tat += process_tat
        process.tat = process_tat
    return total_tat / len(finished_process)


def avg_wt(finished_process):
    total_wt = 0
    for process in finished_process:
        process_wt = process.tat - process.bt  # wt formula
        total_wt += process_wt
        process.wt = process_wt
    return total_wt / len(finished_process)


class Scheduler:
    def __init__(self, process):
        self.process = process
        self.finished_process = []
        self.start_time = 0
        self.end_time = 0

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
                for process in self.process:
                    # filter processes based on arrival time
                    if process.at <= current_time:
                        arrived_process.append(process)
                        print(f"p{process.pid}: {process.remaining_time}", sep='')
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

    def rr(self):
        # round robin
         if not self.process:  # leave if empty
            return

        current_time = 0

        while self.process:
            for process in self.process:
                if process.remaining_time > 0:
                    print("time:", current_time)
                    print("running process: p", process.pid, sep='')
                    print("____________________")

                    if process.remaining_time > quantum:
                        current_time += quantum
                        process.remaining_time -= quantum
                    else:
                        current_time += process.remaining_time
                        process.remaining_time = 0
                        process.ft = current_time
                        self.finished_process.append(process)
                        self.process.remove(process)
                        break  # break out of inner loop to recheck for new processes

        print("time:", current_time)
        print("Running finished\n")

        #print("average response time: ", avg_rt(self.finished_process))
        print("average turn around time: ", avg_tat(self.finished_process))
        print("average waiting time: ", avg_wt(self.finished_process))


    def srtf(self):
        # shortest remaining time first

        if not self.process:    # leave if empty
            return

        # self.start_timer()      # start timer
        current_time = 0

        while self.process:
            arrived_process = []

            print("time:", current_time, "\n")

            if self.process:    # check if list is not empty
                print("arrived processes:")
                for process in self.process:
                    # filter processes based on arrival time
                    if process.at <= current_time:
                        arrived_process.append(process)
                        print(f"p{process.pid}: {process.remaining_time}", sep='')
            else:
                print("No processes in the list")

            # for process in arrived_process:
            #     print(f"p{process.pid}")

            print(" ")

            if not arrived_process:
                # if no processes arrived
                # next_arrival = float('inf')     # infinity
                # for process in self.process:
                #     if process.at < next_arrival:
                #         # find the least arrival time
                #         next_arrival = process.at
                next_arrival = min(process.at for process in self.process)
                current_time = next_arrival
                continue

            shortest_process = None
            shortest_time = float('inf')  # infinity

            # choose the shortest remaining time process
            for process in arrived_process:
                if process.remaining_time < shortest_time:
                    shortest_process = process
                    shortest_time = process.remaining_time
                    if shortest_process.remaining_time == shortest_process.bt:
                        shortest_process.first_started = current_time

            print("running process: p", shortest_process.pid, sep='')
            print("____________________")

            current_time += 1  # increment time
            shortest_process.remaining_time -= 1    # decrement process time

            if shortest_process.remaining_time == 0:
                # procees complete
                shortest_process.ft = current_time     # store finish time
                self.finished_process.append(shortest_process)      # add to finished processes
                arrived_process.remove(shortest_process)    # remove from arrival list
                self.process.remove(shortest_process)  # Remove from process list

        print("time:", current_time, "\n")
        print("Running finished\n")

        print("average response time: ", avg_rt(self.finished_process))
        print("average turn around time time: ", avg_tat(self.finished_process))
        print("average waiting time: ", avg_wt(self.finished_process))
        # finish_time = self.stop_timer()
        # return finish_time

    def mlfq(self):
        # custom algorithm
        pass

    # def start_timer(self):
    #     # Start timer
    #     # self.start_time = time.time()
    #     return self.start_time
    #
    # def stop_timer(self):
    #     # stop timer and return elapsed time
    #     # self.end_time = time.time()
    #     return self.end_time - self.start_time


def read_file(file):
    # read input file and create list
    pass


def random_file(file):
    # generate random file
    pass


process = [Process(1, 0, 8, 0),
           Process(2, 1, 4, 0),
           Process(3, 2, 9, 0),
           Process(4, 3, 5, 0)]

process1 = []

scheduler = Scheduler(process)
#scheduler.srtf()
#scheduler.pp()
scheduler.rr(quantum=3)


# print(finish_time)
