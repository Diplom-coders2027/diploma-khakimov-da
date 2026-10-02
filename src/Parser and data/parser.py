import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

url = "https://www.thefinals.wiki/wiki/Gadgets"  # та, что открыта у тебя в браузере
headers = {"User-Agent": "Mozilla/5.0"}

def get_page(url, headers, retries=3, delay=2):
    """Скачивает страницу. Возвращает HTML или None, если не удалось."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 404:
                print(f"404: страница не найдена -> {url}")
                return None                      # повторять нет смысла

            response.raise_for_status()          # 500 и другие ошибки -> исключение
            return response.text                 # всё хорошо

        except requests.exceptions.HTTPError as e:
            print(f"Ошибка сервера ({e}), попытка {attempt}/{retries}")
        except requests.exceptions.RequestException as e:
            print(f"Проблема соединения ({e}), попытка {attempt}/{retries}")

        time.sleep(delay * attempt)              # ждём всё дольше: 2с, 4с, 6с

    print(f"Не удалось загрузить: {url}")
    return None

html = get_page(url, headers)
if html is None:
    raise SystemExit("Не удалось загрузить главную страницу, выходим")

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
            value = ", ".join(a.get_text(strip=True) for a in td.find_all("a"))
        else:
            value = td.get_text(" ", strip=True)

        if key and value:  # пустые (например, Icon, там только картинка) пропускаем
            stats[key] = value
    return stats

for w in weapons:
    page_html = get_page(w["link"], headers)
    if page_html is None:
        print("Пропускаем:", w["name"])
        continue                                  # переходим к следующему гаджету

    page_soup = BeautifulSoup(page_html, "html.parser")
    w.update(parse_stats(page_soup))
    print("Готово:", w["name"])
    time.sleep(1)

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

print("Всего:", len(weapons))       