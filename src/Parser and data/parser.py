import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

url = "https://www.thefinals.wiki/wiki/Gadgets"  # та, что открыта у тебя в браузере
headers = {"User-Agent": "Mozilla/5.0"}

html = requests.get(url, headers=headers).text
soup = BeautifulSoup(html, "html.parser")

weapons = []
seen = set()

for a in soup.select("a[title]:has(img.mw-file-element)"):
    name = a["title"]
    if name in seen:  # убираем дубли
        continue
    seen.add(name)

    weapons.append({
        "name": name,
        "link": urljoin(url, a["href"]),
        "image": urljoin(url, a.select_one("img")["src"]),
    })

for w in weapons:
    print(w["name"], "-", w["link"])

print("Всего:", len(weapons))

with open("Gadgets.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "link", "image"])
    writer.writeheader()
    writer.writerows(weapons)

def parse_stats(soup):
    stats = {}
    for tr in soup.select("tr.infobox-data"):
        th = tr.find("th")
        td = tr.find("td")
        if not th or not td:
            continue

        key = th.get_text(" ", strip=True)

        # в Build лежит значок "L" + ссылка "Light", нам нужна только ссылка
        if key == "Build" and td.find("a"):
            value = td.find("a").get_text(strip=True)
        else:
            value = td.get_text(" ", strip=True)

        if key and value:  # пустые (например, Icon, там только картинка) пропускаем
            stats[key] = value
    return stats

for w in weapons:
    page = requests.get(w["link"], headers=headers)
    page_soup = BeautifulSoup(page.text, "html.parser")
    w.update(parse_stats(page_soup))
    print("Готово:", w["name"])
    time.sleep(1)  # не нагружаем сайт

# у разных оружий могут быть разные характеристики, собираем все колонки
fieldnames = []
for w in weapons:
    for key in w:
        if key not in fieldnames:
            fieldnames.append(key)

with open("Gadgets.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, restval="")
    writer.writeheader()
    writer.writerows(weapons)    