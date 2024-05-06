import tkinter as tk
from scheduler import Scheduler

class GanttChartGUI:
    def __init__(self, scheduler):
        self.scheduler = scheduler

        self.root = tk.Tk()
        self.root.title("Gantt Chart")

        self.canvas_width = 800
        self.canvas_height = 400
        self.padding = 20

        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.draw_gantt_chart()

        self.root.mainloop()

    def draw_gantt_chart(self):
        y = 50
        current_time = 0
        while self.scheduler.process or self.scheduler.arrived_process or self.scheduler.finished_process:
            self.scheduler.current_time = current_time
            self.scheduler.mlfq()  # Run scheduler until the current time

            for process in self.scheduler.finished_process:
                start_x = self.padding + (process.at - self.scheduler.min_start).days * self.scheduler.day_width
                end_x = self.padding + (process.ft - self.scheduler.min_start).days * self.scheduler.day_width

                self.canvas.create_rectangle(start_x, y, end_x, y + 30, fill='blue')
                self.canvas.create_text(start_x, y + 15, anchor='w', text=f"p{process.pid}")
                y += 40

            current_time += 1  # Increment current time

if __name__ == "__main__":
    S = Scheduler()
    S.read_file('test')

    GanttChartGUI(S)
