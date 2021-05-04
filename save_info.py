from selenium import webdriver
from selenium.webdriver.common.by import By
import inquirer
from bs4 import BeautifulSoup as sp
import time

link = 'https://portal.minv.sk/wps/portal/!ut/p/a1/' \
        'jdFBD4IgGAbgn8QLIcoRygDLnJWrvDRPza2sQ-v3R60O' \
        '1sK-G9vzMt4PUpMtqbvm1h6aa3vumuPjXIs9xzi12QyZkWqE' \
        'UmimoqIAwD3YeYAfo9DPYxlNUVJjdW7AwNkrHwC9fGLX_tLZNLKyXI' \
        'xg6Gf-G_TyRU4FVJWvtZIVg3m_f2yU5fH80ShhcBNtJ7HMASf-ywfAwP42p' \
        'H4SypijeuVJUkoo40TMUk2R0AHg8AKhDk8Q-qRgTURDgJPLqfKzRetadwfspzGT/dl5/d5/L2dBISEvZ0FBIS9nQSEh/'
driver = webdriver.Chrome()
driver.get(link)
driver.find_element(By.ID, 'langSK').click()
time.sleep(3)

current_row = 0
while True:
        time.sleep(1)
        page_src = sp(driver.page_source, 'html.parser')
        form = page_src.find_all('fieldset')[0]
        row = form.find_all('div', 'row')[current_row]
        label = row.find('div', 'key').get_text().strip()
        if '*' in label:
                field = row.find('div', 'value').next_element.next_element
                id = field.get('id')
                if field.name == 'select':
                        question = inquirer.List(id, message=label, choices=[option.text.strip() for option in field.find_all('option')]),
                        answer = inquirer.prompt(question)
                        driver.find_element(By.XPATH, f'//{field.name}[@id="{id}"]/option[text()="{answer}"]').click()
                        current_row+=1
                        continue