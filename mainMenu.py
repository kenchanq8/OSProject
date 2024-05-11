import tkinter as tk
from scheduler import Scheduler
from ganttChartProcess import GanttChartGUI


def run_scheduler(choice):
    if choice == 1:
        output_label.config(text="Running Preemptive Priority\n")
        S.pp()

    elif choice == 2:
        output_label.config(text="Running Round Robin\n")
        S.rr()

    elif choice == 3:
        output_label.config(text="Running Shortest Remaining Time First\n")
        S.srtf()

    elif choice == 4:
        output_label.config(text="Running Multi-Level Feedback Queue\n")
        S.mlfq()

    GanttChartGUI(S, choice)


def on_select():
    selected_option = int(var.get())
    run_scheduler(selected_option)

# Create scheduler
S = Scheduler()
S.read_file('test')

root = tk.Tk()
root.title("Scheduler GUI")

var = tk.StringVar()

options_frame = tk.Frame(root)
options_frame.pack()

options_label = tk.Label(options_frame, text="Select scheduling:")
options_label.pack()

option1 = tk.Radiobutton(options_frame, text="Preemptive priority (PP)", variable=var, value=1)
option2 = tk.Radiobutton(options_frame, text="Round Robin (RR)", variable=var, value=2)
option3 = tk.Radiobutton(options_frame, text="Shortest Remaining Time First (SRTF)", variable=var, value=3)
option4 = tk.Radiobutton(options_frame, text="Multi-level feedback queue Custom algorithm (MLFQ)", variable=var, value=4)

option1.pack(anchor=tk.W)
option2.pack(anchor=tk.W)
option3.pack(anchor=tk.W)
option4.pack(anchor=tk.W)

output_label = tk.Label(root, text="")
output_label.pack()

run_button = tk.Button(root, text="Run", command=on_select)
run_button.pack()

root.mainloop()

