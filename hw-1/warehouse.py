import random
import threading
import time
from queue import Queue

warehouse = Queue()  # Queue в питоне thread-safe


def consumer(num):
    global warehouse

    while True:
        time_to_sleep = random.random() * 7 + 1
        item_num = warehouse.get()
        time.sleep(time_to_sleep)
        print(f"Consumer {num} got item {item_num} from warehouse\nSleep {time_to_sleep} seconds\n")


def producer(num):
    global warehouse

    while True:
        time_to_sleep = random.random() * 7 + 1
        item_num = random.randint(1, 100)
        warehouse.put(item_num)
        time.sleep(time_to_sleep)
        print(f"Producer {num} loaded item {item_num} to warehouse\nSleep {time_to_sleep} seconds\n")


_lock = threading.Lock()

condition = threading.Condition()

consumers_num = int(input("Enter number of consumers: "))
producers_num = int(input("Enter number of producers: "))

consumers = [threading.Thread(name='Thread-1',
                              target=consumer,
                              args=(i,)) for i in range(producers_num)]
producers = [threading.Thread(name='Thread-1',
                              target=producer,
                              args=(i,)) for i in range(producers_num)]

for thread in consumers + producers:
    thread.start()

for thread in consumers + producers:
    thread.join()
