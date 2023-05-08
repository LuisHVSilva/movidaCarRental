from time import sleep

from movida import Search

open_web = False # True -> Open web page while selenium works. False -> Hide web page while selenium works
rental = True  # Decide if the rental will happen in automotive way.

city = "Londrina"

j = 0

stop = Search(open_web, rental).car_value()
print(stop)



"""
while j < 100:

    sleep(300)
    j += 1
"""