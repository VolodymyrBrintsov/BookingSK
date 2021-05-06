from selenium import webdriver
from selenium.webdriver.common.by import By
import inquirer
from bs4 import BeautifulSoup as sp
import time
import json

link = 'https://portal.minv.sk/wps/portal/!ut/p/a1/' \
        'jdFBD4IgGAbgn8QLIcoRygDLnJWrvDRPza2sQ-v3R60O' \
        '1sK-G9vzMt4PUpMtqbvm1h6aa3vumuPjXIs9xzi12QyZkWqE' \
        'UmimoqIAwD3YeYAfo9DPYxlNUVJjdW7AwNkrHwC9fGLX_tLZNLKyXI' \
        'xg6Gf-G_TyRU4FVJWvtZIVg3m_f2yU5fH80ShhcBNtJ7HMASf-ywfAwP42p' \
        'H4SypijeuVJUkoo40TMUk2R0AHg8AKhDk8Q-qRgTURDgJPLqfKzRetadwfspzGT/dl5/d5/L2dBISEvZ0FBIS9nQSEh/'
driver = webdriver.Firefox()
driver.get(link)
driver.find_element(By.ID, 'langSK').click()
buttons = ['submitter1', 'submitter2-print', 'submitter2-isfine']
banned_label = ['Účel pobytu *', 'Kategória pobytu *']

current_row = 0
current_field = 0

button_num = 0
time.sleep(3)
src = driver.page_source

person_name = input('Registration for: ')
registration_fields = {}
while button_num<3:
        src = driver.page_source
        page_src = sp(src, 'html.parser')
        form = page_src.find_all('fieldset')[current_field]
        rows = form.find_all('div', 'row')
        if current_row == len(rows):
                driver.find_element(By.ID, buttons[button_num]).click()
                time.sleep(5)
                try:
                        error = driver.find_element(By.XPATH, "//li[@class='msg error']")
                        print('Error was found')
                except:
                        print('Error was not found')
                        if button_num == 1:
                                window_before = driver.window_handles[0]
                                driver.switch_to.window(window_before)
                        registration_fields[buttons[button_num]] = ['button']
                        button_num += 1
                current_row = 0
                current_field += 1
                continue
        row = rows[current_row]
        if row.parent.get('class')[0] == 'hidden':
                current_row += 1
                continue
        field = row.find('div', 'value').next_element.next_element
        field_id = field.get('id')
        try:
                label = driver.find_element(By.XPATH, f"//label[@for='{field_id}']").text.strip()
        except:
                current_row += 1
                continue
        name = field.name
        if '*' in label and label not in banned_label:
                if name == 'select':
                        options = driver.find_element(By.XPATH, f'//{name}[@id="{field_id}"]').find_elements(By.TAG_NAME, 'option')
                        question = inquirer.List(field_id, message=label, choices=[option.text.strip() for option in options][1:], carousel=True),
                        answer = inquirer.prompt(question)
                        driver.find_element(By.XPATH, f'//{name}[@id="{field_id}"]/option[text()="{answer[field_id]}"]').click()

                elif name == 'input':
                        question = [inquirer.Text(field_id, message=label)]
                        answer = inquirer.prompt(question)
                        driver.find_element(By.XPATH, f'//{name}[@id="{field_id}"]').send_keys(answer[field_id])

                registration_fields[field_id] = [answer[field_id], name]
                current_row += 1
        else:
                current_row += 1

with open('data.json', 'r+') as file:
    data = json.load(file)
file.close()

with open('data.json', 'w+') as file:
    data[person_name] = registration_fields
    json.dump(data, file)
file.close()
