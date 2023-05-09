from time import sleep
from retrying import retry
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from make_up_for import Rental
from send_email import Mail
import constants
import webconnection
from location_informations import Information


class Search:
    def __init__(self, open_web, automatic_rental, email, city):
        self.open_web = open_web
        self.automatic_rental = automatic_rental
        self.email = email
        self.city = city

        # Private class
        self.driver = None
        self.location_dic = None

    def __get_driver(self):
        return self.driver

    def __set_driver(self, driver):
        self.driver = driver

    def __get_location_dic(self):
        return self.location_dic

    def __set_location_dic(self, location_dic):
        self.location_dic = location_dic

    def __login(self):
        print("Making login")
        driver = webconnection.create_driver(constants.login_url, self.open_web)
        driver.find_element(By.ID, "mat-input-0").send_keys(constants.CPF)
        driver.find_element(By.ID, "mat-input-1").send_keys(constants.movida_password)
        button = driver.find_elements(By.TAG_NAME, 'button')
        for i in button:
            if i.text == "Entrar":
                i.click()

        sleep(3)
        return driver

    # Manipulating the location that user wants to rental the car.
    # Ver um jeito de trabalhar com o json para conseguir mudar esses dados
    def __location(self):
        print("Putting your location")
        codigo = self.__get_location_dic()['codigo']
        self.__get_driver().execute_script("document.getElementsByName('loja_iata')[0]"
                                           ".setAttribute('value', '" + self.__get_location_dic()['codigo'] + "')")
        self.__get_driver().execute_script("document.getElementsByName('loja_iata_id')[0]"
                                           ".setAttribute('value', '" + self.__get_location_dic()['id'] + "')")
        self.__get_driver().execute_script("document.getElementsByName('cordx')[0]"
                                           ".setAttribute('value', '" + self.__get_location_dic()['lat'] + "')")
        self.__get_driver().execute_script("document.getElementsByName('cordy')[0]"
                                           ".setAttribute('value', '" + self.__get_location_dic()['lng'] + "')")
        self.__get_driver().execute_script("document.getElementsByName('loja_is24h')[0]"
                                           ".setAttribute('value', '" + self.__get_location_dic()['is24h'] + "')")

    def __removal(self):
        print("Putting removal hour")
        self.__get_driver().find_element(By.ID, "data_retirada").click()
        Select(self.__get_driver().find_element(By.CLASS_NAME, "pika-select-month")).select_by_value("5")

        tag_html_td = 'td[data-day="7"]'
        self.__get_driver().execute_script(
            "document.querySelector('" + tag_html_td + "')"".setAttribute('class', 'is-selected')")
        self.__get_driver().execute_script(
            "document.querySelector('" + tag_html_td + "').setAttribute('aria-selected', 'true')")
        self.__get_driver().find_element(By.ID, "data_retirada").click()
        self.__get_driver().find_element(By.CSS_SELECTOR, tag_html_td).find_element(By.TAG_NAME, "button").click()

        Select(self.__get_driver().find_element(By.ID, "hora_retirada")).select_by_value("21:30")  # Hora

    # Manipulating the rental devolution date.
    def __devolution(self):
        print("Putting devolution hour")
        self.__get_driver().find_element(By.ID, "data_devolucao").click()
        Select(self.__get_driver().find_elements(By.CSS_SELECTOR, "div.pika-single")[1]
               .find_element(By.CLASS_NAME, "pika-select-month")).select_by_value("5")

        tag_html_td = 'td[data-day="11"]'
        self.__get_driver().execute_script(
            "document.getElementsByClassName('pika-single')[1]"
            ".querySelector('" + tag_html_td + "')"
                                               ".setAttribute('class', 'is-selected')"
        )
        self.__get_driver().execute_script(
            "document.getElementsByClassName('pika-single')[1]"
            ".querySelector('" + tag_html_td + "')"
                                               ".setAttribute('aria-selected', 'true')")

        self.__get_driver().find_element(By.ID, "data_devolucao").click()
        self.__get_driver().find_elements(By.CSS_SELECTOR, "div.pika-single")[1].find_element(By.CSS_SELECTOR,
                                                                                              tag_html_td).click()

    def driver_web(self):
        if self.automatic_rental:
            driver = self.__login()
            webconnection.http_code(constants.search_url)
        else:
            url = constants.search_url
            driver = webconnection.create_driver(url, self.open_web)

        self.__set_driver(driver)

    # Create the dictionary of all possibles cars and the price of them.
    def car_value(self):
        self.__set_location_dic(Information(self.city).search_possible_location_json())
        self.driver_web()
        self.__location()
        self.__removal()
        self.__devolution()

        self.__get_driver().find_element(By.CLASS_NAME, "search-button").click()

        print("Making your dictionary")
        car_name = self.__get_driver().find_elements(By.CLASS_NAME, "text-transform--initial")
        car_value = self.__get_driver().find_elements(By.CLASS_NAME, "clube-price__value-discount--size_walk")
        dic = {}
        j = 0

        for i in range(len(car_name)):
            if not car_name[i].text == "":
                dic[car_name[i].text] = car_value[j].text
                j += 2

        if self.automatic_rental:
            Rental().make_up_for(dic, self.__get_driver())
        elif self.email and not self.automatic_rental:
            Mail(car_name, car_value).send()
        else:
            print("The car and value is: " + str(dic))
