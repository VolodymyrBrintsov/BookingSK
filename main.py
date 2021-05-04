from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Book:
    def __init__(self):
        self.link = 'https://portal.minv.sk/wps/portal/!ut/p/a1/' \
                    'jdFBD4IgGAbgn8QLIcoRygDLnJWrvDRPza2sQ-v3R60O' \
                    '1sK-G9vzMt4PUpMtqbvm1h6aa3vumuPjXIs9xzi12QyZkWqE' \
                    'UmimoqIAwD3YeYAfo9DPYxlNUVJjdW7AwNkrHwC9fGLX_tLZNLKyXI' \
                    'xg6Gf-G_TyRU4FVJWvtZIVg3m_f2yU5fH80ShhcBNtJ7HMASf-ywfAwP42p' \
                    'H4SypijeuVJUkoo40TMUk2R0AHg8AKhDk8Q-qRgTURDgJPLqfKzRetadwfspzGT/dl5/d5/L2dBISEvZ0FBIS9nQSEh/'
        self.driver = webdriver.Chrome()
        self.driver.get(self.link)
        self.wait = WebDriverWait(self.driver, 10)
        self.first_page_selectors = [
            {'id': 'f1-citizenship', 'text': 'Ukrajina'},
            {'id': 'f1-purpose-of-stay', 'text': 'Dlhodobý pobyt'},
            {'id': 'f1-previous-permit', 'text': 'Nie'},
            {'id': 'f1-department-name-select', 'text': 'OCP Prešov'}
        ]

    def book(self):
        self.driver.find_element(By.ID, 'langSK').click()
        self.__fill_first_page()

    def __fill_first_page(self):
        for i in range(len(self.first_page_selectors)):
            selector = self.first_page_selectors[i]
            element = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//select[@id='{selector['id']}']/option[text()='{selector['text']}']")))
            element.click()
        self.driver.find_element(By.ID, 'submitter1').click()


Book().book()