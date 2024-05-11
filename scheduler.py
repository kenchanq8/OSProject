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
        self.process = []
        self.arrived_process = []
        self.finished_process = []
        self.current_process = None
        self.previous_process = None
        self.current_time = 0
        self.quantum = None  # rr quantum (taken from file)
        self.qnt1 = QUANTUM1  # queue 1 quantum
        self.qnt2 = QUANTUM2  # queue 2 quantum
        self.Q1 = []  # queue level 1 rr
        self.Q2 = []  # queue level 2 rr
        self.Q3 = []  # queue level 3 fcfs

    def draw_gantt_chart(self, ax, choice, level=None):
        print("Start drawing Gantt chart")

        yticks = []
        ylabels = []

        # Calculate the height and spacing of each process bar
        bar_height = 0.1
        y_spacing = 0
        if not level:
            # Draw finished processes
            for process in self.finished_process:
                start_times = process.start_times
                end_times = process.end_times
                remaining_times = process.remaining_times

                for i in range(len(start_times)):
                    start = start_times[i]
                    end = end_times[i]
                    remaining = remaining_times[i]
                    duration = end - start

                    # Plot the rectangle
                    ax.barh(y=process.pid * (bar_height + y_spacing), left=start, width=duration, height=bar_height,
                            align='center', label=f"Process {process.pid}", color='cyan')

                    if choice != 1:
                        # Add process label
                        ax.text(start + duration / 2, process.pid * (bar_height + y_spacing) + bar_height / 2,
                                f"p{process.pid}: {remaining}", ha='center', va='center')

                    else:
                        # Add process label
                        ax.text(start + duration / 2, process.pid * (bar_height + y_spacing) + bar_height / 2,
                                f"p{process.pid}\n\n", ha='center', va='center')

                        # Add remaining time and priority on top of the segment
                        priority = process.priority  # Get priority of the process
                        ax.text(start + duration / 2, process.pid * (bar_height + y_spacing) + bar_height / 2,
                                f"({remaining}, {priority})", ha='center', va='center')

                    # Add yticks and labels
                    yticks.append(process.pid * (bar_height + y_spacing) + bar_height / 2)
                    ylabels.append(f"p{process.pid}")
        else:
            # Draw finished processes
            for process in self.finished_process:
                start_times = process.start_times
                end_times = process.end_times
                remaining_times = process.remaining_times

                for i in range(len(start_times)):
                    start = start_times[i]
                    end = end_times[i]
                    remaining = remaining_times[i]
                    duration = end - start

                    if process.level_history:
                        # Iterate through level history
                        for i in range(len(process.level_history) - 1):
                            start_time, start_level = process.level_history[i]
                            end_time, end_level = process.level_history[i + 1]
                            # Draw the process if it was running in the specified level during this interval
                            if start_level == level:
                                duration = end_time - start_time
                                # Draw the process bar
                                ax.barh(process.pid, duration, left=start_time, height=bar_height,
                                        label=f"Queue {start_level}")
                                # Add process label
                                ax.text(start_time + duration / 2, process.pid, f"Process {process.pid}",
                                    ha='center', va='center', color='black')

        # Set yticks and ylabels
        ax.set_yticks(yticks)
        ax.set_yticklabels(ylabels)

        # Debugging
        print("Gantt chart drawing completed.")
        return

    # DONE TESTING
    def read_file(self, file):
        with open(file, 'r') as f:
            self.quantum = int(f.readline().strip())  # Read the quantum value from the first line

            for line in f:
                x = line.split()
                pid, at, bt, priority = map(int, x)
                P = process.Process(pid, at, bt, priority)
                self.process.append(P)

    # DONE TESTING GUI
    def pp(self):
        # Preemptive Priority
        if not self.process:  # leave if empty
            return False

        while self.process or self.arrived_process:

            print("time:", self.current_time, "\n")

            for process in self.process[:]:
                if process.at <= self.current_time:
                    self.arrived_process.append(process)
                    self.process.remove(process)

            if not self.arrived_process:
                # If no processes arrived
                next_arrival = min(process.at for process in self.process)
                self.current_time = next_arrival
                continue

            # Sort arrived processes based on remaining time
            for i in range(len(self.arrived_process)):
                min_i = i
                for j in range(i + 1, len(self.arrived_process)):
                    if self.arrived_process[j].priority < self.arrived_process[min_i].priority:
                        min_i = j
                self.arrived_process[i], self.arrived_process[min_i] = \
                    self.arrived_process[min_i], self.arrived_process[i]

            for process in self.arrived_process:
                print(f"p{process.pid}: ({process.remaining_time}, {process.priority})", sep='')

            print(" ")

            # Set current running process to the first arrived process
            self.current_process = self.arrived_process[0]

            if self.current_process.remaining_time == self.current_process.bt:
                self.current_process.first_started = self.current_time

            if self.current_process != self.previous_process:
                # Record the start time when the process starts running
                self.current_process.start_running(self.current_time)
                if self.previous_process:
                    self.previous_process.end_running(self.current_time - 1)

            print("running process: p", self.current_process.pid, sep='')
            print("____________________")

            self.current_time += 1  # Increment time
            self.current_process.remaining_time -= 1  # Decrement process time
            self.previous_process = self.current_process

            if self.current_process.remaining_time == 0:
                # Process complete
                self.current_process.ft = self.current_time  # Store finish time
                self.finished_process.append(self.current_process)  # Add to finished processes
                self.arrived_process.remove(self.current_process)  # Remove from arrival list
                self.current_process.end_running(self.current_time - 1)

        # Print averages
        self.end_print()

    # DONE TESTING GUI
    def rr(self):
        # Round-Robin

        current_process_qtimer = self.quantum  # Set timer for current running process

        while self.process or self.arrived_process:
            print("time:", self.current_time, "\n")

            if self.process:  # Check if list is not empty
                for process in self.process[:]:  # Loop over all process
                    # Add process to arrived process list and remove from processes list
                    if process.at <= self.current_time:
                        self.arrived_process.append(process)
                        self.process.remove(process)

            # Print all arrived processes with their remaining time
            if self.arrived_process:
                print("arrived processes:")
                for process in self.arrived_process:
                    print(f"p{process.pid}: {process.remaining_time}", sep='')

                print(" ")

                # Set current running process to the first arrived process
                self.current_process = self.arrived_process[0]

                if self.current_process.remaining_time > 0:
                    # qnt not finished
                    if current_process_qtimer > 0:
                        print("running process: p", self.current_process.pid, sep='')
                        print("____________________")

                        # Record first started
                        if self.current_process.remaining_time == self.current_process.bt:
                            self.current_process.first_started = self.current_time

                        if self.current_process != self.previous_process:
                            # Record the start time when the process starts running
                            self.current_process.start_running(self.current_time)

                        current_process_qtimer -= 1  # Decrement quantum timer for process
                        self.current_process.remaining_time -= 1  # Decrement remaining time for process

                        # Process finished
                        if self.current_process.remaining_time == 0:
                            self.finished_process.append(self.current_process)  # Add process to finished list
                            self.arrived_process = self.arrived_process[1:]  # Remove current and push elems
                            self.current_process.ft = self.current_time + 1  # Record finish time
                            current_process_qtimer = self.quantum
                            self.current_process.end_running(self.current_time)

                        # Got switched without finishing
                        if current_process_qtimer == 0:
                            self.arrived_process = self.arrived_process[1:]  # Remove first element
                            self.current_process.end_running(self.current_time)

                            # Add process arriving next iteration before the currently switched process
                            for process in self.process[:]:
                                if process.at == (self.current_time + 1):  # Check for arriving processes
                                    self.arrived_process.append(process)  # Add process to arrived process list
                                    self.process.remove(process)  # Remove process from process list
                                    # (avoids repetition in the arrived process list)

                            self.arrived_process.append(self.current_process)  # Read switched process
                            current_process_qtimer = self.quantum  # Reset quantum timer

                self.previous_process = self.current_process
                self.current_time += 1  # Increment timer

            # No processes passed
            else:
                print("No processes arrived")

        # Print averages
        self.end_print()

    # DONE TESTING GUI
    def srtf(self):
        # Shortest remaining time first

        if not self.process:  # Empty process passed
            return False

        while self.process or self.arrived_process:
            print("time:", self.current_time, "\n")
            if self.process:  # Check if list is not empty
                for process in self.process[:]:
                    # Filter processes based on arrival time
                    if process.at <= self.current_time:
                        self.arrived_process.append(process)  # Add to arrived processes
                        self.process.remove(process)  # Remove from process list

            # Print all arrived processes with their remaining time
            if self.arrived_process:
                print("arrived processes:")

                # Print arrived processes
                for process in self.arrived_process:
                    print(f"p{process.pid}: {process.remaining_time}", sep='')

                # Sort arrived processes based on remaining time
                for i in range(len(self.arrived_process)):
                    min_i = i
                    for j in range(i + 1, len(self.arrived_process)):
                        if self.arrived_process[j].remaining_time < self.arrived_process[min_i].remaining_time:
                            min_i = j
                    self.arrived_process[i], self.arrived_process[min_i] = \
                        self.arrived_process[min_i], self.arrived_process[i]
                print(" ")

                # Chooses the shortest process
                self.current_process = self.arrived_process[0]

                # Record process first started time
                if self.current_process.remaining_time == self.current_process.bt:
                    self.current_process.first_started = self.current_time

                if self.current_process != self.previous_process:
                    # Record the start time when the process starts running
                    self.current_process.start_running(self.current_time)  # Record start time for drawing

                # Print running process
                print("running process: p", self.current_process.pid, sep='')
                print("____________________")

                self.current_time += 1  # Increment time
                self.current_process.remaining_time -= 1  # Decrement process remaining time
                self.previous_process = self.current_process

                # Procees complete
                if self.current_process.remaining_time == 0:
                    self.current_process.ft = self.current_time  # Store finish time
                    self.finished_process.append(self.current_process)  # Add to finished processes
                    self.arrived_process = self.arrived_process[1:]  # Remove from arrival list
                    self.current_process.end_running(self.current_time - 1)  # Record end time for drawing

            # No arrived processes
            else:
                self.current_time += 1  # Increment time
                self.previous_process = self.current_process

        # Print averages
        self.end_print()

    # DONE
    def fcfs_ca(self, Q, level):
        # Empty process passed
        if not Q:
            return

        print("time:", self.current_time, "\n")

        # Print arrived processes in queues
        print_arrived(self.Q1, 1)
        print_arrived(self.Q2, 2)
        print_arrived(self.Q3, 3)

        self.current_process = Q[0]

        # Record start time
        if self.current_process.remaining_time == self.current_process.bt:
            self.current_process.first_started = self.current_time
            self.current_process.update_queue_level(self.current_time, level)

        if self.current_process != self.previous_process:
            # Record the start time when the process starts running
            self.current_process.start_running(self.current_time)

        # Print running process
        print("running process: p", self.current_process.pid, sep='')
        print("____________________")
        self.current_process.Qwaited = 0

        self.current_process.remaining_time -= 1  # Decrement process remaining time

        # Procees complete
        if self.current_process.remaining_time <= 0:
            self.current_process.ft = self.current_time  # Store finish time
            self.finished_process.append(self.current_process)  # Add to finished processes
            Q = Q[1:]  # Remove from arrival list
            self.current_process.end_running(self.current_time)

        self.previous_process = self.current_process
        self.current_time += 1  # Increment timer
        return Q

    # DONE
    def mlfq(self):
        # No processes delivered
        if not self.process:
            return False

        while self.process or self.arrived_process or self.Q1 or self.Q2 or self.Q3:
            # Add all arrived processes in list
            for process in self.process[:]:
                if process.at <= self.current_time:  # Process arrived
                    self.arrived_process.append(process)
                    self.process.remove(process)

            if self.arrived_process:
                # Sort arrived processes in queues
                self.sort_process_in_queues()

            if self.Q1:
                # Run algorithm
                self.Q1, self.Q2, self.qnt1, done_process = self.custom_algorithm(self.Q1, self.Q2, self.qnt1, 1)

                # Reset quantum
                if self.qnt1 == 0 or done_process:
                    self.qnt1 = QUANTUM1

                # Checking for process priority update
                self.upgrade_priority(self.Q1, self.Q1, level=1)
                self.upgrade_priority(self.Q2, self.Q1, level=1)
                self.upgrade_priority(self.Q3, self.Q2, level=2)

            elif self.Q2:
                if self.Q1:  # Q1 is not empty
                    continue

                # Run algorithm
                self.Q2, self.Q3, self.qnt2, done_process = self.custom_algorithm(self.Q2, self.Q3, self.qnt2, 2)

                # Reset quantum
                if self.qnt2 == 0 or done_process:
                    self.qnt2 = QUANTUM2

                # Checking for process priority update
                self.upgrade_priority(self.Q2, self.Q1, level=1)
                self.upgrade_priority(self.Q3, self.Q2, level=2)

            elif self.Q3:  # If Q1 or Q2 is not empty
                if self.Q1 or self.Q2:
                    continue

                # Run algorithm
                self.Q3 = self.fcfs_ca(self.Q3, 3)

                # Checking for process priority update
                self.upgrade_priority(self.Q3, self.Q2, level=2)

        # Print averages
        self.end_print()

    # DONE
    def custom_algorithm(self, Qcurrent, Qnext, qnt, level):
        # Printing time and arrived processes
        print("time:", self.current_time, "\n")
        print_arrived(self.Q1, 1)
        print_arrived(self.Q2, 2)
        print_arrived(self.Q3, 3)

        done_process = None  # Reset flag

        if qnt > 0:
            self.current_process = Qcurrent[0]
            # Process not finished
            if self.current_process.remaining_time > 0:
                print("running process: p", Qcurrent[0].pid, sep='')
                print("____________________")
                Qcurrent[0].Qwaited = 0

                # Record first started
                if self.current_process.remaining_time == self.current_process.bt:
                    self.current_process.first_started = self.current_time
                    self.current_process.update_queue_level(self.current_time, level)

                if self.current_process != self.previous_process:
                    # Record the start time when the process starts running
                    self.current_process.start_running(self.current_time)

                qnt -= 1  # dDcrement quantum timer for process
                self.current_process.remaining_time -= 1  # Decrement remaining time for process

                # Process finished
                if self.current_process.remaining_time == 0:
                    self.finished_process.append(self.current_process)  # Add process to finished list
                    self.current_process.ft = self.current_time + 1  # Record finish time
                    Qcurrent = Qcurrent[1:]  # Remove process and push others
                    done_process = True
                    self.current_process.end_running(self.current_time)

                # Add to next queue and remove process from current queue
                elif qnt <= 0:
                    if Qcurrent:
                        Qnext.append(Qcurrent[0])
                        Qcurrent = Qcurrent[1:]
                        self.current_process.end_running(self.current_time)

            self.previous_process = self.current_process
            self.current_time += 1  # Increment timer

            return Qcurrent, Qnext, qnt, done_process

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
        # End of running queue
        print("\nrunning finished at time", self.current_time)

        # Calculate averages
        print("\naverage response time: %.1f" % avg_rt(self.finished_process))
        print("average turn around time time: %.1f" % avg_tat(self.finished_process))
        print("average waiting time: %.1f" % avg_wt(self.finished_process))
        print("")

    def upgrade_priority(self, Qlow, Qhigh, level):
        # Increment the time processes are waiting
        if Qlow and self.current_process:
            for p in Qlow:
                if p.pid != self.current_process.pid:
                    p.Qwaited += 1
                    if p.Qwaited >= 15:
                        Qlow.remove(p)
                        Qhigh.append(p)
                        p.Qwaited = 0

                        # Update queue level of process
                        p.update_queue_level(self.current_time, level)
