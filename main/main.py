from time import sleep

import movida


open_web = True  # True -> Open web page while selenium works. False -> Hide web page while selenium works
automatic_rental = True  # Decide if the rental will happen in automotive way.
email = True
city = "Londrina Aeroporto"

j = 0

while j < 100:
    movida.Search(open_web, automatic_rental, email, city).car_value()
    sleep(300)
    j += 1
