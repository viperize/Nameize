# :\\__ Nameize v0.21 [Roblox Name Generator]
# :\\__ Viperize - MIT License
#--------------------------------------------------------------------------------
# | Imports

import requests, os, ast, threading
from time import sleep
from random import shuffle
from datetime import datetime

#--------------------------------------------------------------------------------
# | Colour Coding

os.system("")

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

#--------------------------------------------------------------------------------
# | Initialisation

name_list, chunked_list = list(), list()

try:
    nameize = requests.get("https://gist.githubusercontent.com/viperize/81ad22f8bef40e76fc7bab176d77815e/raw/bb86c90e5fb2ed628aeebbb7bb43b1e97e0c480c").text
except:
    nameize = "NAMEIZE"

print(style.GREEN + f"{nameize}\n----------------------------------" + style.RED + "\nWARNING: Due to rate limits, until proxy support is added it's advised to use one thread" + style.RESET)

try:
    nl_req = requests.get("https://gist.githubusercontent.com/viperize/b66da66a62f724b3c8ce08ca4d1cde00/raw/da3ceae1c46359f676b6520e7eb162d13cb688ff/").text
    name_list = ast.literal_eval(nl_req)
    shuffle(name_list)
except:
    print(style.RED + "Namelist was unable to load, program will not function correctly" + style.RESET)

counter, finished, final_list = 0, False, []

#--------------------------------------------------------------------------------
# | Functions

def sendtoDiscord(name):
    data = {
        "username": "Nameize",
        "embeds": [
            {
                "title": f"**{name}**",
                "url": "https://github.com/viperize/Nameize",
                "color": 706405,
                "footer": {
                    "text": str(counter)
                },
                "timestamp": str(datetime.now())
            }
        ]
    }
    try:
        requests.post(d_webhook, json=data)
    except Exception as e:
        print(style.RED + f"Err sending data to webhook: {e}" + style.RESET)

def check_moderation(moderated_list):
    global counter, final_list
    for name in moderated_list:
        try:
            mr = requests.get(f"https://auth.roblox.com/v2/usernames/validate?request.username={name}&request.birthday=01%2F01%2F2000&request.context=Signup").json()
            if mr["code"] == 0:
                counter += 1
                print(style.GREEN + f"{counter}) {name} added" + style.RESET)
                with open("./names.txt", "a") as f:
                    f.write(f"{name}\n")
                final_list.append(name)
                if d_webhook:
                    sendtoDiscord(name)
            else:
                print(style.RED + f"{name} has been moderated" + style.RESET)
        except Exception as e:
            print(style.RED + f"Err with moderation status: {e}" + style.RESET)

def usergen(users_wanted, thread_num):
    global counter, finished, final_list
    moderated_list = []
    thread_namelist = chunked_list[thread_num]
    iter_num = 0

    while counter < users_wanted:
        #add words
        userlist = thread_namelist[iter_num:iter_num+40]
        iter_num += 40

        #check if exist
        payload = {"usernames": userlist}
        if debugging:
            print(f"Payload: {userlist}")
        try:
            sleep(payload_delay)
            nr = requests.post("https://users.roblox.com/v1/usernames/users", data=payload).json()
            nr["data"]
        except KeyError:
            print(style.RED + "Rate limited: Sending requests too fast, pausing" + style.RESET)
            if iter_num-40 >= 0:
                iter_num -= 40
            sleep(10)
        except Exception as e:
            print(style.RED + f"Err with payload: {e}" + style.RESET)

        listbx = []
        try:
            for name in nr["data"]:
                listbx.append(name["requestedUsername"])
            moderated_list = [x for x in userlist if x not in listbx]
        except:
            moderated_list = []
        if debugging:
            print(style.YELLOW + f"Moderation: {moderated_list}" + style.RESET)

        #check if moderated
        if not finished and moderated_list:
            check_moderation(moderated_list)
    
    if not finished:
        finished = True
        sleep(5)
        final_list = str(final_list).replace("'","").replace("[","").replace("]","")
        print(style.CYAN + f"\nCompleted {counter} name/s in {round((datetime.now()-time_started).seconds/60)} minutes: {final_list}" + style.RESET)

def userinputs():
    global wanted_users, thread_amount, debugging, payload_delay, d_webhook
    try:
        wanted_users = int(input("How many users do you want? "))
        if wanted_users <= 0:
            raise Exception("Invalid number of users")

        thread_amount = int(input("How many threads? (1-10) (1 recommended) "))
        if thread_amount <= 0 or thread_amount > 10:
            raise Exception("Invalid thread count")

        payload_delay = int(input("Insert payload delay (1300ms recommended) "))
        if payload_delay <= 0:
            raise Exception("Invalid payload delay")
        payload_delay /= 1000

        debugging = input("Would you like to display payloads? (y/n, 'n' is recommended) ")
        if not(debugging.lower() == "y" or debugging.lower() == "n"):
            raise Exception("Invalid debugging input")
        if debugging.lower() == "y":
            debugging = True
        else:
            debugging = False

        discord = input("Would you like to use a webhook? (y/n) ")
        if not(discord.lower() == "y" or discord.lower() == "n"):
            raise Exception("Invalid debugging input")
        if discord.lower() == "y":
            with open("./webhook.txt") as f:
                try:
                    f_url = f.read()
                    wr = requests.get(f_url).json()
                    if wr["token"]:
                        d_webhook = f_url
                    else:
                        raise Exception("Invalid discord webhook")
                except Exception as e:
                    print(style.RED + f"Err with webhook: {e}" + style.RESET)

    except Exception as e:
        print(style.RED + str(e) + style.RESET)
        userinputs()

#--------------------------------------------------------------------------------
# | Initialisation [2]

userinputs()
print(style.GREEN + "----------------------------------" + style.RESET)

t_count = round(len(name_list)/thread_amount)
chunked_list = [name_list[i:i+t_count] for i in range(0, len(name_list), t_count)]
time_started = datetime.now()

threads = list()
for i in range(thread_amount):
    x = threading.Thread(target=usergen, args=(wanted_users, i))
    threads.append(x)
    x.start()

for index, thread in enumerate(threads):
    thread.join()
