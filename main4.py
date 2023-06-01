import httpx as requests
import time
base_url = "http://192.168.4.1/kodzamkato/5038"
start_number = 0
end_number = 10000
output_file = "invalid_numbers.txt"

while True:
    for number in range(start_number, end_number):
        url = base_url + str(number).zfill(4)
        response = requests.get(url)
        if response.text != "NIE TEN KOD":
            with open(output_file, "a") as file:
                file.write(str(number) + "\n")
            print(f"Invalid URL: {url}. Number written to {output_file}.")
        else:
            print(f"Valid URL: {url}")
            # You can add additional logic here based on the response if needed
            break
    else:
        continue  # Continue the while loop if no valid URL is found
    break  # Break the while loop if a valid URL is found
    