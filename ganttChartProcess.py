# gantt_chart_gui.py
import matplotlib.pyplot as plt


class GanttChartGUI:
    def __init__(self, scheduler, choice):
        self.scheduler = scheduler
        self.choice = choice

        if 0 < choice < 4:
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

    def draw_process(self, ax, process, level):
        """
        Draw a process on the Gantt chart.
        """
        for i in range(len(process.level_history) - 1):
            start_time, start_level = process.level_history[i]
            end_time, end_level = process.level_history[i + 1]
            if start_level == level:  # Process was running in this queue level
                ax.barh(level, end_time - start_time, left=start_time, align='center', color='blue', alpha=0.5)
                ax.text(start_time + (end_time - start_time) / 2, level, f'P{process.pid}',
                        ha='center', va='center', color='black')
