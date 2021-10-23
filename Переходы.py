from collections import defaultdict
import requests
import time
import threading
from threading import Thread

lo, hi = 99701, 99711

all_rc_ids = [ i for i in range(lo, hi) ]

current_state_of_controllers = dict.fromkeys(all_rc_ids)
cycle_of_rc = defaultdict(list)

def alert(ident, state):
    print(f'КОТРОЛЛЕР {ident} ПЕРЕХОДИТ В СОСТОЯНИЕ {state}')

def listen(ident):
    url = f"https://api.via-dolorosa.ru/rc/{ident}/status"
    
    while True:
        time.sleep(1)
        response = requests.get(url)
    
        try:
            response.raise_for_status()
            
            current = response.json()
            current_phase = current['current_phase_id']
            
            previuos = current_state_of_controllers[ident]
            if (previuos is None) or (previuos['current_phase_id'] != current_phase):
                cycle_of_rc[ident].append( current_phase )
                current_state_of_controllers[ident] = current
                
                
                
                print(f"Контроллер {ident}, состояния: {cycle_of_rc[ident]}")
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
    

for ident in range(lo, hi):
    th = Thread(target=listen, args=(ident,))
    th.start()
