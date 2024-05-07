# gantt_chart_gui.py
import matplotlib.pyplot as plt

class GanttChartGUI:
    def __init__(self, scheduler, choice):
        self.scheduler = scheduler
        self.choice = choice

        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        scheduler.draw_gantt_chart(self.ax, choice)

        if 0 < choice < 4:
            plt.title("Gantt Chart")
            plt.xlabel("Time")
            plt.ylabel("Processes")
            plt.grid(True)
            plt.show()
            return
