import tkinter as tk
from datetime import datetime, timedelta

def create_gantt_chart(canvas, tasks):
    canvas_width = 800
    canvas_height = 200
    bar_height = 30
    padding = 20
    text_padding = 5

    max_end = max(task['end'] for task in tasks)
    min_start = min(task['start'] for task in tasks)
    total_days = (max_end - min_start).days

    day_width = (canvas_width - 2 * padding) / total_days

    for i, task in enumerate(tasks):
        start_date = task['start']
        end_date = task['end']
        duration = end_date - start_date

        start_x = padding + (start_date - min_start).days * day_width

        # Draw task bar
        canvas.create_rectangle(start_x, padding + i * bar_height, start_x + duration.days * day_width, padding + (i + 1) * bar_height, fill='blue')
        canvas.create_text(start_x, padding + (i + 1) * bar_height + text_padding, anchor='sw', text=task['name'])

        # Draw start date text
        canvas.create_text(start_x, padding + (i + 1) * bar_height + text_padding * 2, anchor='nw', text=start_date.strftime("%Y-%m-%d"))

def show_gantt_chart(tasks):
    root = tk.Tk()
    root.title("Gantt Chart")

    canvas = tk.Canvas(root, width=800, height=200)
    canvas.pack()

    create_gantt_chart(canvas, tasks)

    root.mainloop()

# Example tasks
tasks = [
    {'name': 'Task 1', 'start': datetime(2024, 5, 1), 'end': datetime(2024, 5, 5)},
    {'name': 'Task 2', 'start': datetime(2024, 5, 3), 'end': datetime(2024, 5, 8)},
    {'name': 'Task 3', 'start': datetime(2024, 5, 6), 'end': datetime(2024, 5, 10)}
]

show_gantt_chart(tasks)
