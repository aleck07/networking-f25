import threading
import time

ranges = [
    [10, 20],
    [1, 5],
    [70, 80],
    [27, 92],
    [0, 16]
]

def compute_nums(name, start, end, result):
    """ Compute the nums of the given array. """

    total = 0
    intArray = range(start, end + 1)
    for num in intArray:
        total += num
    print(f"{name} computed sum: {total}")
    result[int(name[-1])] = total
    return total 

# We need to keep track of them so that we can join() them later. We'll
# put all the thread references into this array
threads = []
result = [0] * len(ranges)  # Create an array of `n` zeros

# Launch all threads!!
for i, rangeArr in enumerate(ranges):

    name = f"Thread{i}"

    t = threading.Thread(target=compute_nums, args=(name, rangeArr[0], rangeArr[-1], result))
    t.start()
    threads.append(t)

# Join all the threads back up to this, the main thread. The main thread
# will block on the join() call until the thread is complete. If the
# thread is already complete, the join() returns immediately.

for t in threads:
    t.join()

sum = 0
for num in result:
    sum = sum + num

print(f"Total sum computed by all threads: {sum}")  