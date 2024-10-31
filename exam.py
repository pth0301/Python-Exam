import requests
import argparse
import subprocess
import html
import os
import re
path = 'exploits-db'

# --exploit argument
def exploit_func(id):
    # take exploit_content from exploit-db(stored in folder) when users can access by id
    pattern = r'^\d+$' # check input 
    found = False
    if re.match(pattern, id):
        for file in os.listdir(path):
            file_id = os.path.splitext(file)[0]
            if file_id == id: # if available in exploit-db -> display directly
                found = True
                print("Retrieve data from exploits-db...")
                file_path = os.path.join(path, file)
                
                # Check if the file exists before trying to open it
                if os.path.isfile(file_path):
                    os.system(f"notepad {file_path}")  # Open the file in Visual Studio Code
                break 
            
        if not found: # if not available in exploits-db -> send request to exploit-db.com by using URL
            print("Waiting for reponse from exploit-db.com ...")
            url = 'https://exploit-db.com/exploits/{}'.format(id)
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            res= requests.get(url, headers = headers)
            exploit = res.text[res.text.find('<code') : res.text.find('</code>')]
            exploit = html.unescape(exploit[exploit.find('">') +2 :])
            # print(exploit)
            temp_file_path = os.path.join(path, 'temp_exploit.txt')
            with open(temp_file_path, 'w') as temp_file:
                temp_file.write(exploit)
            os.system(f"notepad {temp_file_path}")

        

    else:
        print("Invalid ID!")

            
# --page argument: return all list stored in corresponding page
pages = []
lst = [elem.replace(".txt", "") for elem in os.listdir(path)]
def page_func(id): # id - number of page -> return 5 exploits in 1 page
    try:
        count = 0
        page = []
        for file in lst:
            page.append(file)
            count+=1
            if count == 5:
                pages.append(page)
                count = 0
                page = list()
            
        for exploit in pages[id]:
            print(exploit)
    except Exception as e:
        print("An error ocured: ", e)


# --search argument: search keyworks from content of exploits stored by using regex to process searching
def search_func(keyword):
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.findall(rf'\b{keyword.replace(" ", "|")}\b', content)
            if match:
                print(full_path)


def main():
    # Initialize instance ArgumentParser
    parser = argparse.ArgumentParser(
    prog = 'exam.py',
    description = 'Python Exam'
    )
    # Add optional argument
    parser.add_argument('--exploit', type=str, help='exploit ID')
    parser.add_argument('--page', type=int, help='get page')
    parser.add_argument('--search', type=str, help='search keyword')
    
    # parser argument
    args = parser.parse_args()
    # function
    if args.exploit:
        exploit_func(args.exploit)
    elif args.page is not None:
        page_func(args.page)
    elif args.search:
        search_func(args.search)
    else:
        parser.print_help()
    # parser.exit()
   

# input
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("An error ocured: ", e)

    # exploit_id = input("Enter the exploit id: ")
    # check input 
    # pattern = r'^\d+$'
    # if re.match(pattern, exploit_id):
    #     exploit_func(exploit_id)
    # else:
    #     print("ID is not correct with format")
    
    # check page_func
    # page_func(int(exploit_id))
    
    # # search_func(search) -> check search_func
    # keyword = input("keyword searched: ")
    # search_func(keyword)