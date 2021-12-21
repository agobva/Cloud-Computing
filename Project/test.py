import random
import json
from typing import Counter
import requests
import time
import threading

def thread_function(args, t, arr):
    e = False
    url = 'https://b550fkp3tl.execute-api.eu-north-1.amazonaws.com/SortingProjectDV1566/'

    try:
        t0 = time.time()
        r = requests.post(url, data=json.dumps(arr))
        t1 = time.time()
    except Exception as error:
        e = True
        args.append(str(error))
    if not e:
        args.append(r.status_code)
        t.append(round(t1-t0, 2))


iterations = [600, 600, 600, 600, 600, 600]


for iteration in iterations:
    x = set()
    res = []
    t = []

    for i in range(iteration):
        random.seed(0)
        arr = [random.randint(0,100000) for i in (sorted(range(3000), reverse=True))]
        x.add(threading.Thread(target=thread_function, args=(res, t, arr)))

    t0 = time.time()
    for i, x_ in enumerate(x):
        try:
            x_.start()
        except:
            print("Failed to start thread: " + i)
            x.remove(x_)

    for x_ in x:
        x_.join()

    t1 = time.time()

    print(f"Concurrent User: {iteration}")
    for k,v in Counter(res).items():
        print(f"\t{k}: {v}")

    print(f"Max: {max(t)}")
    print(f"Min: {min(t)}")
    print(f"Avg: {sum(t)/len(t)}")
    print(f"Total: {round(t1-t0, 2)}\n")

    time.sleep(60)

