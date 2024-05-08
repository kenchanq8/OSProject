# gantt_chart_gui.py
import matplotlib.pyplot as plt


class GanttChartGUI:
    def __init__(self, scheduler, choice):
        self.scheduler = scheduler
        self.choice = choice

        if 0 < choice < 3:
            self.fig, self.ax = plt.subplots(figsize=(20, 10))
            scheduler.draw_gantt_chart(self.ax, choice)

            plt.title("Gantt Chart")
            plt.xlabel("Time")
            plt.ylabel("Processes")
            plt.grid(True)
            plt.show()
            return
        elif choice == 4:
            self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3)
            scheduler.draw_gantt_chart(self.ax1, choice, level=1)
            scheduler.draw_gantt_chart(self.ax2, choice, level=2)
            scheduler.draw_gantt_chart(self.ax3, choice, level=3)

            # Enable grid
            self.ax1.grid(True)
            self.ax2.grid(True)
            self.ax3.grid(True)

            plt.title("Gantt Chart")
            plt.xlabel("Time")
            plt.ylabel("Processes")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
            return
