import httpx
import time
from itertools import product

string = "1234567890"

# Generate all combinations and print them
for i in range(1, len(string) + 1):
    for combination in product(string, repeat=i):
        print(''.join(combination))
        kod = ''.join(combination)
        response = httpx.get(f'http://192.168.4.1/kodzamkato/50{kod}')
        print(response.text)
        if not response.text == "NIE TEN KOD":
          break
        # time.sleep(1)