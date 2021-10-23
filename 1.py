import requests
import time
import threading
from threading import Thread
import tkinter as tk

template = "Контроллер {}, статус: {}, фаза: {}"

root = tk.Tk()
root.title('Проверка контроллеров')
root.geometry('600x400')
labels = dict()

for id in range(99701, 99711):
    labels[id] = tk.Label(root)
    labels[id].pack()

def check_rc(id):
    url = f"https://api.via-dolorosa.ru/rc/{id}/status"
    
    while True:
        time.sleep(5)
        response = requests.get(url)
    
        try:
            response.raise_for_status()
            data = response.json()
            labels[id].config(text = template.format(id, data['status'], data['current_phase_id']))
            root.update()
            time.sleep(1)
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
    

for id in range(99701,99711):
    th = Thread(target=check_rc, args=(id,))
    th.start()

root.mainloop()
