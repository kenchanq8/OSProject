class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.at = arrival_time
        self.bt = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.first_started = None
        self.ft = None
        self.wt = None
        self.tat = None
        self.rt = None
