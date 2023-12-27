import requests
import asyncio
from proxyhub import Broker
from colorama import Fore
import os
import argparse
from queue import Queue
import random
import warnings

warnings.filterwarnings("ignore")

def cls():
  if os.name == "nt":
    os.system("cls")
  elif os.name == "posix":
    os.system("clear")

cls()

banner = """ 
.____                  __    ________          __          
|    |    ____ _____  |  | __\______ \ _____ _/  |______   
|    |  _/ __ \\__  \ |  |/ / |    |  \\__  \\   __\__  \  
|    |__\  ___/ / __ \|    <  |    `   \/ __ \|  |  / __ \_
|_______ \___  >____  /__|_ \/_______  (____  /__| (____  /
        \/   \/     \/     \/        \/     \/          \/    v1.0

                           by aktas
                  https://github.com/aktas                                                
"""
print(f"{Fore.RED}{banner}\n{Fore.RESET}")

ap = argparse.ArgumentParser()
ap.add_argument('-e', '--email', required=True, help="Target email address")
ap.add_argument('-p', '--proxy', action='store_true', help='Proxy will be used')

args = vars(ap.parse_args())

if "@" in args['email']:
   username = (args['email']).split("@")[0]
else:
   username = args['email']

if args['proxy'] == True:
   print(f"{Fore.GREEN}[*]{Fore.RESET} Searching for proxy ")

   proxy_list_queue = Queue()

   async def show(proxies):
      while True:
            proxy = await proxies.get()
            if proxy is None: break
            if (proxy.is_working == True):
               proxy_list_queue.put({'http': f'{proxy.host}:{proxy.port}'})
               print(f"{Fore.GREEN}[*]{Fore.RESET} Proxy set to {proxy.host}:{proxy.port}")
               break


   proxies = asyncio.Queue()
   broker = Broker(proxies)
   tasks = asyncio.gather(
      broker.find(types=['HTTP', 'HTTPS'], limit=10),
      show(proxies)
   )

   loop = asyncio.get_event_loop()
   loop.run_until_complete(tasks)

   proxy_list = proxy_list_queue.get()
else:
   proxy_list = {}

print(f"{Fore.GREEN}[*]{Fore.RESET} Searching for Leak data from username.")

browser_list = [
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/118.0"
]
browser = random.choice(browser_list)
params = {"query": username}
headers = {
    "User-Agent": "curl/7.68.0"
}
url = f'https://api.proxynova.com/comb'
try:
   response = requests.get(url, params=params, headers=headers, timeout=10, proxies=proxy_list)
   if "Why have I been blocked?" in response.text:
      print(f"{Fore.GREEN}[*]{Fore.RESET} You are blocked for sending too many requests!")
   else:
      if ("application/json" in response.headers.get("Content-Type", "")) and response.json()['count'] > 0:
         for i in response.json()['lines']:
            print(f"{Fore.RED}*******{Fore.RESET}")
            print(f"{Fore.GREEN}[*]{Fore.RESET} Found : {i}")
      else:
         print(f"{Fore.GREEN}[*]{Fore.RESET} No results found!")
except:
   print(f"{Fore.GREEN}[*]{Fore.RESET} The server is too busy!")

print(f"{Fore.RED}*******{Fore.RESET}")
print(f"""{Fore.RED}
  //
 ('>
 /rr     r4bbIt hoL3
*\))_
""")
print(f"{Fore.RED}*******{Fore.RESET}")

print(f"{Fore.GREEN}[!]{Fore.RESET} Searching for Leak data from email.")

url = "https://data-leak-check.cybernews.com/chk/email"


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Content-Type': 'application/json',
    'Origin': 'https://cybernews.com/',
    'Sec-Fetch-Dest': 'empty',
}

data = '{"email":"' + args['email'] + '"}'
try:
   response = requests.post('https://data-leak-check.cybernews.com/chk/email', headers=headers, data=data, verify=False)
   if ("application/json" in response.headers.get("Content-Type", "")):
      if len(response.json()['dataLeakEmails']) > 0:
         for i in response.json()['dataLeakEmails']:
            print(f"{Fore.RED}*******{Fore.RESET}")
            print(f"{Fore.GREEN}[*]{Fore.RESET} Domain : {i['name']}")
            print(f"{Fore.GREEN}[*]{Fore.RESET} Published : {i['published']}")
      else:
         print(f"{Fore.GREEN}[*]{Fore.RESET} No results found!")
   else:
      print(f"{Fore.GREEN}[*]{Fore.RESET} The server is too busy!")
except:
   print(f"{Fore.GREEN}[*]{Fore.RESET} The server is too busy!")

