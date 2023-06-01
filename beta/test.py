import threading
import queue

def generate_numbers(start, end, result_queue):
    numbers = []
    for i in range(start, end):
        numbers.append(i)
    result_queue.put(numbers)

def main():
    start = 1
    end = 100
    num_threads = 4  # Number of threads to use
    numbers = []

    # Calculate the range for each thread
    range_size = (end - start) // num_threads

    # Create a queue to hold the results from each thread
    result_queue = queue.Queue()

    # Create and start the threads
    threads = []
    for i in range(num_threads):
        thread_start = start + (i * range_size)
        thread_end = thread_start + range_size

        # The last thread should handle any remaining numbers
        if i == num_threads - 1:
            thread_end = end

        # Create a new thread with the target function and arguments
        thread = threading.Thread(target=generate_numbers, args=(thread_start, thread_end, result_queue))
        threads.append(thread)

        # Start the thread
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Consolidate the results from the queue
    while not result_queue.empty():
        numbers.extend(result_queue.get())

    # Print the generated numbers
    print(numbers)

if __name__ == '__main__':
    main()
