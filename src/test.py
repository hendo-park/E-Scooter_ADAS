import datetime
import time

t = datetime.datetime.now().time()
t=str(t)
print(t)


t1 = time.time()
time.sleep(1.5)
t2 = time.time()
print(t2-t1)