import os
import requests
from bs4 import BeautifulSoup
import html

# Set the base URL for exploits on exploit-db.com
BASE_URL = "https://www.exploit-db.com/exploits/"
SAVE_FOLDER = "./exploits-db"  

# Ensure the folder exists
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def fetch_exploit_content(exploit_id):
    url = f"{BASE_URL}{exploit_id}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser') #parsing html

        # Find the code snippet, typically within a <code> tag
        code_block = soup.find('code')
        try:
            # Unescape HTML entities and return content
            exploit_content = html.unescape(code_block.get_text())
            return exploit_content
        except:
            print("Could not find exploit code.")
            return None
    else:
        print("Failed to retrieve page.")
        return None

def store_exploit_content(exploit_id, content):
    filename = os.path.join(SAVE_FOLDER, f"{exploit_id}.txt")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Exploit saved to {filename}")
    return filename

# Main Function
if __name__ == '__main__':
    for exploit_id in range(1997, 2000):
        exploit_content = fetch_exploit_content(exploit_id)

        if exploit_content:
            file_path = store_exploit_content(exploit_id, exploit_content)

