from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import datetime

data_file = open('data.json', 'r+', encoding='utf-8')
data = json.load(data_file)
data_file.close()

link = 'https://portal.minv.sk/wps/portal/!ut/p/a1/' \
        'jdFBD4IgGAbgn8QLIcoRygDLnJWrvDRPza2sQ-v3R60O' \
        '1sK-G9vzMt4PUpMtqbvm1h6aa3vumuPjXIs9xzi12QyZkWqE' \
        'UmimoqIAwD3YeYAfo9DPYxlNUVJjdW7AwNkrHwC9fGLX_tLZNLKyXI' \
        'xg6Gf-G_TyRU4FVJWvtZIVg3m_f2yU5fH80ShhcBNtJ7HMASf-ywfAwP42p' \
        'H4SypijeuVJUkoo40TMUk2R0AHg8AKhDk8Q-qRgTURDgJPLqfKzRetadwfspzGT/dl5/d5/L2dBISEvZ0FBIS9nQSEh/'
driver = webdriver.Firefox()
driver.get(link)
wait = WebDriverWait(driver, 10)
driver.find_element(By.ID, 'langSK').click()

def find_error():
    try:
        return driver.find_element(By.XPATH, "//li[@class='msg error']")
    except:
        return None

def save_file(data):
    data_file = open('data.json', 'w+', encoding='utf-8')
    data[person]['status'] = 'disabled'
    json.dump(data, data_file, indent=4)
    data_file.close()

for person, selectors in data.items():
    try:
        if selectors['status'] == 'enabled':
            for selector_name, selector_value in selectors.items():
                if selector_value[-1] == 'select':
                    wait.until(EC.presence_of_element_located((By.XPATH, f"//select[@id='{selector_name}']/option[text()='{selector_value[0]}']"))).click()
                elif selector_value[-1] == 'input':
                    wait.until(EC.presence_of_element_located((By.XPATH, f"//input[@id='{selector_name}']"))).send_keys(selector_value[0])
                elif selector_value[-1] == 'button':
                    wait.until(EC.presence_of_element_located((By.XPATH, f"//input[@id='{selector_name}']"))).click()
                    time.sleep(5)

            window_before = driver.window_handles[0]
            driver.switch_to.window(window_before)

            wait.until(EC.presence_of_all_elements_located((By.XPATH, "//select[@id='appointment-date-requested']//*")))[-1].click()
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='submitter3']"))).click()
            time.sleep(5)
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='sms-phone-number']"))).send_keys('+421951387947')
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='submitter4']"))).click()
            time.sleep(5)
            error = find_error()
            print(error)
            if error:
                freetime = driver.find_elements(By.XPATH, '//select[@id="available-dates"]//*')[1].text
                date, start_time, _, finish_time = freetime.split(' ')
                start_time = datetime.datetime.strptime(f'{date} {start_time}', '%d.%m.%Y %H:%M')
                finish_time = datetime.datetime.strptime(f'{date} {finish_time}', '%d.%m.%Y %H:%M')
                fifteen_minutes = datetime.timedelta(minutes=5)
                while start_time < finish_time or not error:
                    start_time += fifteen_minutes
                    driver.execute_script(f"document.getElementById('appointment-date-final').value = '{start_time.strftime('%d.%m.%Y %H:%M')}'")
                    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='submitter4']"))).click()
                    time.sleep(5)
                    error = find_error()
            if not error:
                save_file(data)
    except:
        pass