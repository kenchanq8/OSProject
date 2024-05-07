# import time
#
# def start_timer():
#     """Starts the timer."""
#     return time.time()
#
# def stop_timer(start_time):
#     """Stops the timer and returns the elapsed time."""
#     return time.time() - start_time
#
# # Example usage:
# start_time = start_timer()
#
# # Do something that takes time
# time.sleep(2)
#
# elapsed_time = stop_timer(start_time)
# print("Elapsed time:", elapsed_time, "seconds")

# list = [1]
# list = list[1:]
# for i in range(len(list)):
#     print(list[i])

import matplotlib.pyplot as plt

# Function to draw Gantt chart
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

def draw_gantt_chart(ax):
    # Sample data for processes
    processes = [
        {"pid": 1, "start": 0, "duration": 5},
        {"pid": 2, "start": 2, "duration": 4},
        {"pid": 3, "start": 6, "duration": 3},
        {"pid": 4, "start": 9, "duration": 6}
    ]

    # Plotting Gantt chart for each process
    for process in processes:
        ax.barh(y=process["pid"], width=process["duration"], left=process["start"], height=0.5, align='center')
        ax.text(process["start"] + process["duration"] / 2, process["pid"], f"Process {process['pid']}",
                ha='center', va='center')

    # Set labels and title
    ax.set_xlabel('Time')
    ax.set_ylabel('Process ID')
    ax.set_title('Gantt Chart')

    # Set yticks
    ax.set_yticks([process["pid"] for process in processes])
    ax.set_yticklabels([f"Process {process['pid']}" for process in processes])

    # Set x-axis limits
    ax.set_xlim(0, max(process["start"] + process["duration"] for process in processes) + 1)

# Create a new figure and axes
fig, (ax1, ax2) = plt.subplots(2)

# Draw Gantt chart for the first axes
draw_gantt_chart(ax1)

# Draw Gantt chart for the second axes
draw_gantt_chart(ax2)

# Adjust layout to prevent overlapping
plt.tight_layout()

# Show the plot
plt.show()




