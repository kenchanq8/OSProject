# main.py
from scheduler import Scheduler
from ganttChartProcess import GanttChartGUI

if __name__ == "__main__":
    S = Scheduler()
    S.read_file('/Users/drmad/PycharmProjects/OSProject/test')

    GanttChartGUI(S)
