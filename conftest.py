import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


@pytest.fixture(autouse=True)
def browser():
    driver = webdriver.Chrome()
    # service = Service(GeckoDriverManager().install())
    # driver = webdriver.Firefox(service=service)

    driver.set_window_size(1400, 1000)

    yield driver

    driver.quit()

