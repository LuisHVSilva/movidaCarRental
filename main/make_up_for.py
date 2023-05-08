from time import sleep

from selenium.webdriver.common.by import By
import constants
import datarefactory
from send_email import Mail


class Rental:
    def __init__(self):
        self.driver = None

    def __get_driver(self):
        return self.driver

    def __set_driver(self, driver):
        self.driver = driver

    def make_up_for(self, dic, driver):
        print("Make Up For?")
        self.__set_driver(driver)
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
        sleep(5000000000)
        # driver.execute_script("document.getElementById('concluir_pagamento_reserva').click")
