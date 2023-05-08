import requests
from selenium import webdriver


def http_code(url):
    try:
        requests.get(url) == 200
    except():
        print("Website is not working!")


# Create de drive to make selenium possible. It's necessary for start the python request and get the web html.
def create_driver(url, open_web):
    print("Creating driver")
    http_code(url)
    if open_web:
        driver = webdriver.Edge()

    else:
        options = webdriver.EdgeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Edge(options=options)

    driver.get(url)
    return driver
