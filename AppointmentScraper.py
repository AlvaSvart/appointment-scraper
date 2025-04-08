import time
import requests
from bs4 import BeautifulSoup
from plyer import notification

# URI der Terminbuchung
URL = "https://www.terminland.de/noris-psychotherapie/online/ADHS_new/default.aspx?m=39059&ll=HT7kc&dpp=HIqZ2&dlgid=9&step=3&dlg=1&a2291013099=2291025408&css=1"

# Hinweistext
INFO = "Für die ADHS-Abklärung stehen derzeit keine freien Termine zur Verfügung."

# Zeitintervall (in Sekunden)
INTERVALL = 600

def check_termine():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        card_body = soup.find("div", class_="card-body")

        if card_body:
            text = card_body.get_text(strip=True)
            if INFO in text:
                print("Keine Termine verfügbar.")
            else:
                print("Termine verfügbar!")
                notification.notify(title="Termin verfügbar!", message="Termine verfügbar!", timeout=20)
        else:
            print("Kein <div class='card-body'> gefunden.")
            notification.notify(title="Something changed", message="Termine verfügbar?", timeout=20)

    except Exception as e:
        print(f"Fehler: {e}")

while True:
    check_termine()
    time.sleep(INTERVALL)