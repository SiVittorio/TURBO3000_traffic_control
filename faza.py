import requests
from pprint import pprint
import threading
from threading import Thread
import time
from tkinter import *
import subprocess, platform

def erase_line(): # Очистка консоли
    time.sleep(2)
    if platform.system()=="Windows": # for Windows
        subprocess.Popen("cls", shell=True).communicate()
    else: #Linux and Mac
        print("\033c", end="")
        
def req(id): # Получение данных API с контроллера
    while True:
        time.sleep(2)
        if re.status_code == 200:
            respa=re.json()
            print('Контроллер №',id, ' Статус: ', respa['status_rc'], 'Текущая фаза ', respa['current_phase_id'])
            erase_line()
        elif re.status_code == 404:
            print('NOT AM I WORKING')
        else:
            print('shit!', re.status_code)

for id in range(99701,99711):
    url = "".join(('https://api.via-dolorosa.ru/rc/', str(id), '/status'))
    re = requests.get(url)  
    th=Thread(target=req, args=(id, )) # Создание потока
    th.start() # Старт потока

# Окна, окна, окна...
main = Tk()

main.mainloop()
