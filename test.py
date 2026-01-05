import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.ugent.be/student/nl/studentenleven/resto/menu/weekmenu/week02-brug-sterre"
WEBHOOK_URL = "https://discord.com/api/webhooks/1457683842855993488/LX4CK63gFc19H28yOndS6jvRhWUXGCLxHYc8jsVwlMZ26mxLuPmHwNb-kmRqxG-jo8pQ"

dagen = {
    "Monday": "Maandag",
    "Tuesday": "Dinsdag",
    "Wednesday": "Woensdag",
    "Thursday": "Donderdag",
    "Friday": "Vrijdag",
}

eng = datetime.today().strftime("%A")
if eng not in dagen:
    exit()  # weekend

vandaag = dagen[eng]

html = requests.get(URL).text
soup = BeautifulSoup(html, "html.parser")

bericht = None

for dag in soup.select("div.item.visualIEFloatFix"):
    titel = dag.find("h2")
    if not titel or titel.get_text(strip=True) != vandaag:
        continue

    lijnen = [f"**{vandaag} – De Brug / Sterre**"]

    for section in dag.find_all("h3"):
        lijnen.append(f"\n**{section.get_text()}**")
        ul = section.find_next_sibling("ul")
        if ul:
            for li in ul.find_all("li"):
                lijnen.append(f"- {li.get_text(strip=True)}")

    bericht = "\n".join(lijnen)
    break

if bericht:
    requests.post(WEBHOOK_URL, json={"content": bericht})
