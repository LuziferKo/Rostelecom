import pickle
import time
import pytest
from pages.auth import *
from selenium.webdriver.common.by import By
from pages.settings import valid_phone, valid_email, valid_login, invalid_ls, valid_password, valid_pass_reg


@pytest.mark.auth
@pytest.mark.positive
@pytest.mark.parametrize('username', [valid_phone, valid_email, valid_login, invalid_ls],
                         ids=['phone', 'email', 'login', 'ls'])
def test_active_tab(browser, username):
    """Проверка автоматического переключения табов телефона/email/логина/лицевого счёта
    invalid_ls - номер лицевого счёта валидного формата"""
    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_password)
    if username == valid_phone:
        assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == 'Телефон'
    elif username == valid_email:
        assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == 'Почта'
    elif username == valid_login:
        assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == 'Логин'
    else:
        assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == 'Лицевой счет'


@pytest.mark.auth
@pytest.mark.positive
def test_auth_with_valid_email(browser):
    """Проверка авторизации по почте и паролю"""
    page = AuthPage(browser)
    page.enter_username(valid_email)
    page.enter_password(valid_pass_reg)
    time.sleep(30)  # Время для ввода капчи в случае её появления
    page.btn_click_enter()
    page.driver.save_screenshot('auth_with_email.png')

    with open('my_cookies.txt', 'wb') as cookies:
        pickle.dump(browser.get_cookies(), cookies)

    assert page.get_relative_link() == '/account_b2c/page'


@pytest.mark.auth
@pytest.mark.positive
@pytest.mark.parametrize('username', [valid_phone, valid_login],
                         ids=['valid phone', 'valid login'])
def test_auth_with_valid_login(browser, username):
    """Проверка авторизации по номеру телефона и паролю, проверка автоматического переключения табов телефон/логин
    (для проверки требуется зарегистрированный номер телефона и существующий логин)"""
    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_password)
    page.btn_click_enter()

    assert page.get_relative_link() == '/account_b2c/page'


@pytest.mark.reg
@pytest.mark.positive
def test_open_reg_page(browser):
    """Проверка открытия страницы регистрации (smoke test)"""
    page = AuthPage(browser)
    page.enter_reg_page()

    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'
