import process

# global variables (FOR CUSTOM ALGORITHM DONT REMOVE)
QUANTUM1 = 10
QUANTUM2 = 5


def avg_rt(finished_process):
    # caculate average response time
    total_rt = 0
    for process in finished_process:
        process_rt = process.first_started - process.at  # rt formula
        process.rt = process_rt  # record rt of process
        total_rt += process_rt  # calc total
    return total_rt / len(finished_process)  # return average


def avg_tat(finished_process):
    # caculate average tur around time
    total_tat = 0
    for process in finished_process:
        process_tat = process.ft - process.at  # tat formula
        total_tat += process_tat  # calc total
        process.tat = process_tat  # recording TAT of process
    return total_tat / len(finished_process)  # return average


def avg_wt(finished_process):
    # caculate average wait time
    total_wt = 0
    for process in finished_process:
        process_wt = process.tat - process.bt  # wt formula
        total_wt += process_wt  # calc total
        process.wt = process_wt  # recording wt of process
    return total_wt / len(finished_process)  # return average


def print_arrived(Q, qpriority):
    print(f"Q{qpriority}:")
    if Q:
        for p in Q:
            print(f"\tp{p.pid}: {p.remaining_time}", sep='')
    print(" ")


class Scheduler:
    def __init__(self):
        self.tasks = []
        self.process = []
        self.finished_process = []
        self.current_process = None
        self.arrived_process = []
        self.current_time = 0
        self.quantum = None
        self.qnt1 = QUANTUM1
        self.qnt2 = QUANTUM2
        self.Q1 = []
        self.Q2 = []
        self.Q3 = []

    def read_file(self, file):
        with open(file, 'r') as f:
            self.quantum = int(f.readline().strip())  # Read the quantum value from the first line

            for line in f:
                x = line.split()
                pid, arrival_time, burst_time, priority = map(int, x)
                P = process.Process(pid, arrival_time, burst_time, priority)
                self.process.append(P)

    # DONE TESTING (just add more comments)
    def pp(self):
        # preemptive priority
        if not self.process:  # leave if empty
            return

        while self.process:
            arrived_process = []

            print("time:", self.current_time, "\n")

            if self.process:  # check if list is not empty
                print("arrived processes:")

                # sort processes based on arrival time then priority
                sorted_process = []
                for process in self.process:
                    insert = False
                    for i in range(len(sorted_process)):
                        if process.at < sorted_process[i].at or (process.at == sorted_process[i].at
                                                                 and process.priority < sorted_process[i].priority):
                            sorted_process.insert(i, process)
                            insert = True
                            break
                    if not insert:
                        sorted_process.append(process)
                for process in sorted_process:
                    # filter processes based on arrival time
                    if process.at <= self.current_time:
                        arrived_process.append(process)
                        print(f"p{process.pid}: ({process.remaining_time}, {process.priority})", sep='')
            else:
                print("No processes in the list")

            print(" ")

            if not arrived_process:
                # if no processes arrived
                next_arrival = min(process.at for process in self.process)
                self.current_time = next_arrival
                continue

            Hpriority_process = None
            h_priority = float('inf')  # infinity

            # choice the highest priority process
            for process in arrived_process:
                if process.priority < h_priority:
                    Hpriority_process = process
                    h_priority = process.priority
                    if Hpriority_process.remaining_time == Hpriority_process.bt:
                        Hpriority_process.first_started = self.current_time

            print("running process: p", Hpriority_process.pid, sep='')
            print("____________________")

            self.current_time += 1  # increment time
            Hpriority_process.remaining_time -= 1  # decrement process time

            if Hpriority_process.remaining_time == 0:
                # process complete
                Hpriority_process.ft = self.current_time  # store finish time
                self.finished_process.append(Hpriority_process)  # add to finished processes
                arrived_process.remove(Hpriority_process)  # remove from arrival list
                self.process.remove(Hpriority_process)  # Remove from process list

        # print averages
        self.end_print()

    # DONE TESTING
    def rr(self):
        # round-robin

        # quantum_value = next(self.quantum)
        #
        # # Convert the extracted integer value to an integer
        # quantum_integer = int(quantum_value)
        current_process_qtimer = self.quantum  # set timer for current running process

        while self.process or self.arrived_process:
            print("time:", self.current_time, "\n")

            if self.process:  # check if list is not empty
                for process in self.process[:]:  # loop over all process
                    # add process to arrived process list and remove from processes list
                    if process.at <= self.current_time:
                        self.arrived_process.append(process)
                        self.process.remove(process)

            # print all arrived processes with their remaining time
            if self.arrived_process:
                print("arrived processes:")
                for process in self.arrived_process:
                    print(f"p{process.pid}: {process.remaining_time}", sep='')

                print(" ")

                # set current running process to the first arrived process
                self.current_process = self.arrived_process[0]

                if self.current_process.remaining_time > 0:
                    # qnt not finished
                    if current_process_qtimer > 0:
                        print("running process: p", self.current_process.pid, sep='')
                        print("____________________")

                        # record first started
                        if self.current_process.remaining_time == self.current_process.bt:
                            self.current_process.first_started = self.current_time

                        current_process_qtimer -= 1  # decrement quantum timer for process
                        self.current_process.remaining_time -= 1  # decrement remaining time for process

                        # process finished
                        if self.current_process.remaining_time == 0:
                            self.finished_process.append(self.current_process)  # add process to finished list
                            self.arrived_process = self.arrived_process[1:]  # remove current and push elems
                            self.current_process.ft = self.current_time + 1  # record finish time
                            current_process_qtimer = self.quantum

                        # got switched without finishing
                        if current_process_qtimer == 0:
                            self.arrived_process = self.arrived_process[1:]  # remove first element

                            # add process arriving next iteration before the currently switched process
                            for process in self.process[:]:
                                if process.at == (self.current_time + 1):  # check for arriving processes
                                    self.arrived_process.append(process)  # add process to arrived process list
                                    self.process.remove(process)  # remove process from process list
                                    # (avoids repetition in the arrived process list)

                            self.arrived_process.append(self.current_process)  # read switched process
                            current_process_qtimer = self.quantum  # reset quantum timer

                self.current_time += 1  # increment timer

            # no processes passed
            else:
                print("No processes arrived")

        # print averages
        self.end_print()

    # DONE TESTING
    def srtf(self):
        # shortest remaining time first

        if not self.process:  # empty process passed
            return False

        while self.process or self.arrived_process:
            print("time:", self.current_time, "\n")
            if self.process:  # check if list is not empty
                for process in self.process[:]:
                    # filter processes based on arrival time
                    if process.at <= self.current_time:
                        self.arrived_process.append(process)  # add to arrived processes
                        self.process.remove(process)  # remove from process list

            # print all arrived processes with their remaining time
            if self.arrived_process:
                print("arrived processes:")

                # print arrived processes
                for process in self.arrived_process:
                    print(f"p{process.pid}: {process.remaining_time}", sep='')

                # sort arrived processes based on remaining time
                for i in range(len(self.arrived_process)):
                    min_i = i
                    for j in range(i + 1, len(self.arrived_process)):
                        if self.arrived_process[j].remaining_time < self.arrived_process[min_i].remaining_time:
                            min_i = j
                    self.arrived_process[i], self.arrived_process[min_i] = \
                        self.arrived_process[min_i], self.arrived_process[i]
                print(" ")

                # for p in self.arrived_process:
                #     print(f"p{p.pid}, {p.remaining_time}")

                # chooses the shortest process
                shortest_process = self.arrived_process[0]

                # record process first started time
                if shortest_process.remaining_time == shortest_process.bt:
                    shortest_process.first_started = self.current_time

                # print running process
                print("running process: p", shortest_process.pid, sep='')
                print("____________________")

                self.current_time += 1  # increment time
                shortest_process.remaining_time -= 1  # decrement process remaining time

                # procees complete
                if shortest_process.remaining_time == 0:
                    shortest_process.ft = self.current_time  # store finish time
                    self.finished_process.append(shortest_process)  # add to finished processes
                    self.arrived_process = self.arrived_process[1:]  # remove from arrival list

            # no arrived processes
            else:
                self.current_time += 1  # increment time

        # print averages
        self.end_print()

    # DONE
    def fcfs_ca(self, Q):
        # empty process passed
        if not Q:
            return

        print("time:", self.current_time, "\n")

        # print arrived processes in queues
        print_arrived(self.Q1, 1)
        print_arrived(self.Q2, 2)
        print_arrived(self.Q3, 3)

        # record start time
        if Q[0].remaining_time == Q[0].bt:
            Q[0].first_started = self.current_time

        # print running process
        print("running process: p", Q[0].pid, sep='')
        print("____________________")
        Q[0].Qwaited = 0

        Q[0].remaining_time -= 1  # decrement process remaining time

        # procees complete
        if Q[0].remaining_time <= 0:
            Q[0].ft = self.current_time  # store finish time
            self.finished_process.append(Q[0])  # add to finished processes
            Q = Q[1:]  # remove from arrival list

        self.current_time += 1  # increment timer
        return Q

    # DONE
    def mlfq(self):
        # no processes delivered
        if not self.process:
            return False

        while self.process or self.arrived_process or self.Q1 or self.Q2 or self.Q3:
            # add all arrived processes in list
            for process in self.process[:]:
                if process.at <= self.current_time:  # process arrived
                    self.arrived_process.append(process)
                    self.process.remove(process)

            if self.arrived_process:
                # sort arrived processes in queues
                self.sort_process_in_queues()

            if self.Q1:
                # run algorithm
                self.Q1, self.Q2, self.Q3, self.qnt1, done_process = self.custom_algorithm(self.Q1, self.Q2, self.qnt1,
                                                                                           self.Q3)

                # reset quantum
                if self.qnt1 == 0 or done_process:
                    self.qnt1 = QUANTUM1

                # checking for process priority update
                self.upgrade_priority(self.Q1, self.Q1)
                self.upgrade_priority(self.Q2, self.Q1)
                self.upgrade_priority(self.Q3, self.Q2)

            elif self.Q2:
                if self.Q1:  # Q1 is not empty
                    continue

                # run algorithm
                self.Q2, self.Q3, none_value, self.qnt2, done_process = self.custom_algorithm(self.Q2, self.Q3,
                                                                                              self.qnt2)

                # reset quantum
                if self.qnt2 == 0 or done_process:
                    self.qnt2 = QUANTUM2

                # checking for process priority update
                self.upgrade_priority(self.Q2, self.Q1)
                self.upgrade_priority(self.Q3, self.Q2)

            elif self.Q3:  # if Q1 or Q2 is not empty
                if self.Q1 or self.Q2:
                    continue

                # run algorithm
                self.Q3 = self.fcfs_ca(self.Q3)

                # checking for process priority update
                self.upgrade_priority(self.Q3, self.Q2)

        # print averages
        self.end_print()

    # DONE
    def custom_algorithm(self, Qcurrent, Qnext, qnt, Qlast=None):
        # printing time and arrived processes
        print("time:", self.current_time, "\n")
        print_arrived(self.Q1, 1)
        print_arrived(self.Q2, 2)
        print_arrived(self.Q3, 3)

        done_process = None  # reset flag

        if qnt > 0:
            self.current_process = Qcurrent[0]
            # process not finished
            if Qcurrent[0].remaining_time > 0:
                print("running process: p", Qcurrent[0].pid, sep='')
                print("____________________")
                Qcurrent[0].Qwaited = 0

                # record first started
                if Qcurrent[0].remaining_time == Qcurrent[0].bt:
                    Qcurrent[0].first_started = self.current_time

                qnt -= 1  # decrement quantum timer for process
                Qcurrent[0].remaining_time -= 1  # decrement remaining time for process

                # process finished
                if Qcurrent[0].remaining_time == 0:
                    self.finished_process.append(Qcurrent[0])  # add process to finished list
                    Qcurrent[0].ft = self.current_time + 1  # record finish time
                    Qcurrent = Qcurrent[1:]  # remove process and push others
                    done_process = True

                # add to next queue and remove process from current queue
                if qnt <= 0:
                    if Qcurrent:
                        Qnext.append(Qcurrent[0])
                        Qcurrent = Qcurrent[1:]

            self.current_time += 1  # increment timer

            return Qcurrent, Qnext, Qlast, qnt, done_process

    # DONE
    def sort_process_in_queues(self):
        while self.arrived_process:
            process = self.arrived_process[0]
            if process.bt > self.qnt1:
                process.Qpriority = 1
                self.Q2.append(process)
                self.arrived_process.remove(process)
            elif process.bt > self.qnt2:
                process.Qpriority = 2
                self.Q1.append(process)
                self.arrived_process.remove(process)
            else:
                process.Qpriority = 3
                self.Q3.append(process)
                self.arrived_process.remove(process)

    def end_print(self):
        # end of running queue
        print("\nrunning finished at time", self.current_time)

        # calculate averages
        print("\naverage response time: %.1f" % avg_rt(self.finished_process))
        print("average turn around time time: %.1f" % avg_tat(self.finished_process))
        print("average waiting time: %.1f" % avg_wt(self.finished_process))
        print("")

    def upgrade_priority(self, Qlow, Qhigh):
        # increment the time processes are waiting
        if Qlow and self.current_process:
            for p in Qlow:
                if p.pid != self.current_process.pid:
                    p.Qwaited += 1
                    if p.Qwaited >= 15:
                        Qlow.remove(p)
                        Qhigh.append(p)
                        p.Qwaited = 0
