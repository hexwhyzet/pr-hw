import threading

next_digit = 1


def consumer(cond, digit, repeat):
    global next_digit
    ctr = 0
    while ctr < repeat:
        with cond:
            cond.wait_for(lambda: next_digit == digit)
            print(next_digit)
            ctr += 1
            next_digit = next_digit % 3 + 1
            cond.notify_all()


condition = threading.Condition()

n = int(input("Введите n: "))

t1 = threading.Thread(name='Thread-1',
                      target=consumer,
                      args=(condition, 1, n))
t2 = threading.Thread(name='Thread-2',
                      target=consumer,
                      args=(condition, 2, n))
t3 = threading.Thread(name='Thread-3',
                      target=consumer,
                      args=(condition, 3, n))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()
