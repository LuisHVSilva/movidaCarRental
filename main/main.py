from time import sleep

from movida import Search

open_web = True # True -> Open web page while selenium works. False -> Hide web page while selenium works
rental = True  # Decide if the rental will happen in automotive way.

city = "Londrina"

j = 0


while j < 100:
    stop = Search(open_web, rental).car_value()
    sleep(300)
    j += 1
