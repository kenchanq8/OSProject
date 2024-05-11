# gantt_chart_gui.py
import matplotlib.pyplot as plt


class GanttChartGUI:
    def __init__(self, scheduler, choice):
        self.scheduler = scheduler
        self.choice = choice
        self.fig, self.ax = plt.subplots(figsize=(20, 10))
        scheduler.draw_gantt_chart(self.ax, choice)

        plt.title("Gantt Chart")
        plt.xlabel("Time")
        plt.ylabel("Processes")
        plt.grid(True)
        plt.show()
        return
