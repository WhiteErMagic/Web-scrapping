from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import json

def wait_element(browser, delay_second=1, by=By.CLASS_NAME, value=None):
    return WebDriverWait(browser, delay_second).until(
        expected_conditions.presence_of_element_located((by, value))
    )

if __name__ == '__main__':

    chrome_path = ChromeDriverManager().install()
    options = ChromeOptions()
    options.add_argument('--headless')
    browser_service = Service(executable_path=chrome_path)
    browser = Chrome(service=browser_service, options=options)

    browser.get('https://spb.hh.ru/search/vacancy?text=Python+django+Flask&area=1&area=2')
    #browser.get('https://spb.hh.ru/search/vacancy?text=python&salary=&ored_clusters=true&area=1&area=2&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line')

    # Список блоков вакансий
    vacancies_list = browser.find_elements(By.CLASS_NAME, 'vacancy-serp-item__layout')
    res = []

    for el in vacancies_list:

        # Ссылка на ваканчию
        vacancy_block_link = wait_element(browser=el, by=By.CLASS_NAME, value='serp-item__title-link-wrapper')
        vacancy_link_a = wait_element(browser=vacancy_block_link, by=By.TAG_NAME, value='a')
        vacancy_link = vacancy_link_a.get_attribute('href')

        # Компания и город
        vacancy_block_company_sity = wait_element(browser=el, by=By.CLASS_NAME, value='vacancy-serp-item__info')
        vacancy_block_company = wait_element(browser=el, by=By.CLASS_NAME, value='vacancy-serp-item__meta-info-company')
        vacancy_company_a = wait_element(browser=vacancy_block_company, by=By.TAG_NAME, value='a')
        vacancy_company = vacancy_company_a.text

        vacancy_block_sity = wait_element(browser=el, by=By.XPATH, value='//div[@data-qa="vacancy-serp__vacancy-address"]')
        vacancy_sity = vacancy_block_sity.text
        if "," in vacancy_sity:
            vacancy_sity = vacancy_sity.split(",")[0]

        # Зарплата
        vacancy_block_salary = wait_element(browser=el, by=By.XPATH,
                                          value='//span[@data-qa="vacancy-serp__vacancy-compensation"]')
        vacancy_salary = vacancy_block_salary.text

        res.append({'href': vacancy_link, 'salary': vacancy_salary, 'company': vacancy_company, 'city': vacancy_sity})

    with open('vacancies.json', 'w', encoding='utf-8') as f_out:
        json.dump(res, f_out, ensure_ascii=False)

