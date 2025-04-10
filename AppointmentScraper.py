import time
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service   # Change chrome to firefox
from selenium.webdriver.chrome.options import Options   # Change chrome to firefox
from bs4 import BeautifulSoup
from plyer import notification

# Info text
INFO = "Für die ADHS-Abklärung stehen derzeit keine freien Termine zur Verfügung."

# Time intervall (in Seconds)
INTERVALL = 600

def check_dates():

    # Setup for Chrome
    options = Options()
    options.add_argument("--headless")  # No browser window popping up
    driver = webdriver.Chrome(service=Service("D:\dev\Chromedriver\chromedriver-win64\chromedriver.exe"), options=options)  # Change Chrome to Firefox

    driver.get("https://www.terminland.de/noris-psychotherapie/online/ADHS_new/")
    time.sleep(5)   # Page loading takes a while

    # Check radio button
    radio_btn = driver.find_element(By.CLASS_NAME, "checkmark")
    radio_btn.click()

    # Check next button
    next_btn = driver.find_element(By.ID, "btnGo")
    next_btn.click()

    time.sleep(7)   # Page loading takes even longer sometimes while checking dates
    url = driver.current_url

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        card_body = soup.find("div", class_="card-body")

        if card_body:
            text = card_body.get_text(strip=True)
            if INFO in text:
                print(datetime.datetime.now().strftime("%d.%m.%Y %H:%M"), "Keine Termine verfügbar.")
            else:
                print(datetime.datetime.now().strftime("%d.%m.%Y %H:%M"), "Text hat sich geändert. Termine verfügbar?")
                notification.notify(title="Termin verfügbar!", message="Termine verfügbar!", timeout=20)
        else:
            print(datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),"Kein <div class='card-body'> gefunden. Terminpicker verfügbar?")
            notification.notify(title="Something changed", message="Termine verfügbar?", timeout=20)

        driver.quit()

    except Exception as e:
        print(f"Error: {e}")

while True:
    check_dates()
    time.sleep(INTERVALL)