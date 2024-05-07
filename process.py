class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.at = arrival_time
        self.bt = burst_time
        self.priority = priority
        self.Qwaited = 0
        self.remaining_time = burst_time
        self.first_started = None
        self.ft = None
        self.wt = None
        self.tat = None
        self.rt = None
        self.start_times = []  # List to store start times of each interval
        self.end_times = []  # List to store end times of each interval

    def start_running(self, current_time):
        """
        Record the start time when the process starts running.
        """
        self.start_times.append(current_time)

    def end_running(self, current_time):
        """
        Record the end time when the process finishes running.
        """
        self.end_times.append(current_time+1)
