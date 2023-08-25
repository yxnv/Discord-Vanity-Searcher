import requests
import time
import json

# ANSI escape codes for text color
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_END = '\033[0m'

def main():
    vanity_file = 'vanity.txt'
    valid_file = 'valid.txt'
    
    vanity_urls = read_lines_from_file(vanity_file)
    valid_vanity_urls = set(read_lines_from_file(valid_file))
    
    for vanity_url in vanity_urls:
        vanity_url = vanity_url.strip()
        if vanity_url in valid_vanity_urls:
            print(f"{COLOR_GREEN}Vanity URL {vanity_url} already checked and valid.{COLOR_END}")
            continue
        
        print(f"Checking vanity URL: {vanity_url}")
        
        response = check_vanity_url(vanity_url)
        
        if response is not None:
            print("Response: ", end="")
            if response.get("type") == 0:
                print(f"{COLOR_RED}Not Available{COLOR_END}")
            else:
                print(f"{COLOR_GREEN}Available{COLOR_END}")
                valid_vanity_urls.add(vanity_url)
                save_valid_vanity_to_file(valid_vanity_urls, valid_file)
                print(f"Vanity URL '{vanity_url}' added to valid.txt")
                
        time.sleep(5)  # Sleep for 5 seconds before the next request

def read_lines_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines

def check_vanity_url(vanity_url):
    url = f'https://ptb.discord.com/api/v9/invites/{vanity_url}'
    
    try:
        response = requests.get(url)
        response_json = response.json()
        return response_json
    except Exception as e:
        print(f"Error checking vanity URL {vanity_url}: {e}")
        return None

def save_valid_vanity_to_file(valid_vanity_urls, filename):
    with open(filename, 'w') as file:
        for vanity_url in valid_vanity_urls:
            file.write(vanity_url + '\n')

if __name__ == '__main__':
    main()
