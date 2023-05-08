from time import sleep

from retrying import retry

import webconnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import datarefactory
from send_email import Mail
import constants


class Search:
    def __init__(self, open_web, rental):
        self.open_web = open_web
        self.rental = rental

        # Private class
        self.driver = None

    def __get_driver(self):
        return self.driver

    def __set_driver(self, driver):
        self.driver = driver

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
        self.__set_driver(driver)

    # Manipulating the location that user wants to rental the car.
    # Ver um jeito de trabalhar com o json para conseguir mudar esses dados
    def __location(self):
        print("Putting your location")
        self.__get_driver().execute_script("document.getElementsByName('loja_iata')[0].setAttribute('value', 'LDB')")
        self.__get_driver().execute_script("document.getElementsByName('loja_iata_id')[0].setAttribute('value', '115')")
        self.__get_driver().execute_script("document.getElementsByName('cordx')[0].setAttribute('value', '-23.326438')")
        self.__get_driver().execute_script("document.getElementsByName('cordy')[0].setAttribute('value', '-51.139629')")
        self.__get_driver().execute_script("document.getElementsByName('loja_is24h')[0].setAttribute('value', '0')")

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

    # Create the dictionary of all possibles cars and the price of them.
    @retry
    def car_value(self):
        if self.rental:
            self.__login()
            webconnection.http_code(constants.search_url)
        else:
            url = constants.search_url
            self.__set_driver(webconnection.create_driver(url, self.open_web))

        driver = self.__get_driver()
        self.__location()
        self.__removal()
        self.__devolution()

        driver.find_element(By.CLASS_NAME, "search-button").click()

        print("Making your dictionary")
        car_name = driver.find_elements(By.CLASS_NAME, "text-transform--initial")
        car_value = driver.find_elements(By.CLASS_NAME, "clube-price__value-discount--size_walk")
        dic = {}
        j = 0

        for i in range(len(car_name)):
            if not car_name[i].text == "":
                dic[car_name[i].text] = car_value[j].text
                j += 2

        self.__set_driver(driver)
        return self.__make_up_for(dic)

    def __make_up_for(self, dic):
        print("Make Up For?")
        if datarefactory.str_to_float(dic["208, HB20, ou similar."]) < 100.00:
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("Deu muito bom. Corre pra ver")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            car = "208, HB20, ou similar."
            value = dic["208, HB20, ou similar."]
            self.__define_protections(value)
            Mail(car, value).send()

        elif datarefactory.str_to_float(dic["HB20S, Voyage, Cronos ou Similar."]) < 90.00:
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("Deu muito bom. Corre pra ver")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            car = "HB20S, Voyage, Cronos ou Similar."
            value = dic["HB20S, Voyage, Cronos ou Similar."]
            self.__define_protections(value)
            Mail(car, value).send()

        elif datarefactory.str_to_float(dic["HB20, 208 ou Similar."]) <= 80.00:
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("Deu muito bom. Corre pra ver")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            car = "HB20, 208 ou Similar."
            value = dic["HB20, 208 ou Similar."]
            self.__define_protections(value)
            Mail(car, value).send()

        else:
            print("It does not make up for. We will going to search again in five (5) minutes.")
            print("----------------------------------------------------------------------------------------------")
            print("Não deu bom. Tentando de novo")
            print("----------------------------------------------------------------------------------------------")
            return False

    def __define_protections(self, value):
        print("Defining your protections")
        driver = self.__get_driver()
        driver.find_element(By.CSS_SELECTOR, 'button[data-valor="' + value + '"]').click()
        driver.execute_script("document.getElementsByClassName('pricing')[4].getElementsByTagName('button')[0].click()")
        driver.find_elements(By.CLASS_NAME, "selAvancarReserva")[1].click()
        self.__set_driver(driver)
        self.finish_rental()

    def finish_rental(self):
        print("Finishing your rental")
        driver = self.__get_driver()
        driver.find_element(By.ID, "pagarAgora").click()  # Escolher o pagar agora
        driver.execute_script('document.getElementsByTagName("movida-cartoes")[0]'
                              '.shadowRoot'
                              '.getElementById("' + constants.id_carta__finish_rental + '").click()')
        driver.find_element(By.ID, "numeroCvv").send_keys(constants.CVV)
        driver.find_element(By.CLASS_NAME, "btn-validar").click()
        driver.execute_script("document.getElementById('prePagamento').click()")
        driver.execute_script("document.getElementById('licenca').click()")
        driver.execute_script("document.getElementById('politicaCancelamento').click()")
        # driver.execute_script("document.getElementById('concluir_pagamento_reserva').click")
