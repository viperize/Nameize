# :\\__ RBXNameize [Roblox Name Finder]
# :\\__ Viperize - MIT License
#--------------------------------------------------------------------------------
# | Imports

import requests, os, threading
from time import sleep
from random import choice
from datetime import datetime

#--------------------------------------------------------------------------------
# | Main

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
# | Commands

r = requests.get("https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt")

blacklisted_words = ['sex','shit','fag','cock','cum','homo','breast','tit','puss','weed','loli','pregnant',
'shit','fuck','satan','ass','gay','slave','anal','rape','gass','sperm', 'dick','damn','gang','fack','molester','alcohol',
'nigg','erect','gypsy','porn','suck','holic','tard','feck','clit','gas','corona','wank']
counter = 0
finished = False
final_list = []

def usergen(users_wanted, character_limit, minimum_limit):
    time_started = datetime.now()
    global counter, finished, final_list
    checking = False
    moderated_list = []
    
    while counter < users_wanted:
        #add words
        userlist = []
        while len(userlist) <= 40:
            word = choice(r.text.split("\n")).lower().replace("\r","")
            if not any(bl_word in word for bl_word in blacklisted_words) and (len(word) <= character_limit and len(word) >= minimum_limit):
                userlist.append(word)

        #check if exist
        payload = {"usernames": userlist}
        try:
            nr = requests.post("https://users.roblox.com/v1/usernames/users", data=payload)
            nr = nr.json()
        except Exception as e:
            print(f"Err with payload: {e}")

        listbx = []
        try:
            for name in nr["data"]: 
                listbx.append(name["requestedUsername"])
            new_list = [x for x in userlist if x not in listbx]
            for word in new_list:
                moderated_list.append(word)
        except:
            new_list = []

        #check if moderated
        if not checking:
            checking = True
            for name in moderated_list:
                mr = requests.get(f"https://auth.roblox.com/v2/usernames/validate?request.username={name}&request.birthday=01%2F01%2F2000&request.context=Signup")
                mr = mr.json()
                if not finished:
                    if mr["code"] == 0:
                        counter += 1
                        print(style.GREEN + f"{counter}) {name} added")
                        with open("./names.txt", "a") as f:
                            f.write(f"{name}\n")
                        final_list.append(name)
                    else:
                        print(style.RED + f"{name} has been moderated")
                moderated_list.remove(name)
            checking = False
    
    if not finished:
        finished = True
        sleep(5)
        final_list = str(final_list).replace("'","").replace("[","").replace("]","")
        print(style.CYAN + f"Completed {counter} name/s in {round((datetime.now()-time_started).seconds/60)} minutes: {final_list}")


wanted_users = int(input("How many users do you want? "))
maximum_limit = int(input("Maximum character length? (3-16) "))
minimum_limit = int(input("Minimum character length? (3-16) "))
thread_amount = int(input("How many threads? (1-10) "))

threads = list()
for i in range(thread_amount):
    x = threading.Thread(target=usergen, args=(wanted_users, maximum_limit, minimum_limit))
    threads.append(x)
    x.start()
