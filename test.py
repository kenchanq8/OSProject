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

list = [1]
list = list[1:]
for i in range(len(list)):
    print(list[i])
