import requests
import time
from pprint import pprint
import threading
import pickle


def alert(rc, msg):
    print(f'Контроллер {rc}: {msg}')


URL = 'https://api.via-dolorosa.ru/rc/{}/status'

def find_cycle(rc):
    history = []
    times = []    

    while True:
        response = requests.get(URL.format(rc))

        if response.status_code >= 500:
            alert(rc, 'не отвечает...Повторное соединение...')
            continue
        elif 200 <= response.status_code < 300:
            json = response.json()
            current_phase_id = json['current_phase_id']            
            ti = json['time']

            if not history:
                alert(rc, f'в фазе {current_phase_id} (стартовая позиция)')
                history.append( (current_phase_id, 0) )
                times.append(ti)
                continue

            if history[-1][0] != current_phase_id:
                history.append( (current_phase_id, ti-times[-1]) )
                times.append(ti)

                if len(history) > 3 and history[2][0] == history[-1][0] and abs(history[2][1]-history[-1][1]) <= 5:
                    break

                print(rc, f'перешёл из фазы {history[-2][0]} в фазу {history[-1][0]} за {history[-1][1]} секунд')
        else:
            alert(rc, 'повторное соединение...')

    return history[2:-1]        

def write_bin_file(name, cycle):
    with open(f'{name}.bin', 'wb') as pickle_file:
        pickle.dump(cycle, pickle_file)

def get_period_by_phase(phase, name):
    with open(f"{name}.bin", "rb") as pickle_file:
        records = pickle.load(pickle_file)
        for rec in records:
            if rec[0] == phase:
                return rec[1]
        return None

def main():
    rc1 = 99701

    print(f"Выявление цикла фаз контроллера-{rc1}...\n")

    cycle = find_cycle(rc1)
    print('Цикл программы контроллера успешно найден!\n')
    for (phase, period) in cycle:
        print(f"Фаза {phase}, период={period}")

    write_bin_file(rc1, cycle)
    print('Данные сериализированы!\n')
    
    print(f'Попытка прочесть период 2ой фазы контроллера-{rc1}: ', end="")
    if (r := (get_period_by_phase(2, rc1))) is not None:
        print(r)
    else:
        print("не удалось считать данные")

main()
