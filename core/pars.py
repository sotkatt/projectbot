import json
import requests
from bs4 import BeautifulSoup
from database import create_places

def get_html(url, header):
    r = requests.get(url, headers=header)
    
    if r.status_code == 200:
        return r.text
    
    else:
        return None
    

def processing(html):
    soup = BeautifulSoup(html, 'lxml').find('div', {"class": "impression-items"}).find_all('div', {"class": "impression-card"})
    data = []
    for item in soup:
        if item.get('data-partner'):
            continue

        title = item.get('data-title')
        category = item.get('data-category')
        soup_adress = item.find('div', {'class':'impression-card-info'}).get_text(strip=True)
        minprice = item.get('data-minprice') if item.get('data-minprice') else '0'
        url = item.find('div', {'class': 'impression-card-image'}).find('a').get('href')
        
        # partner = item.get('data-partner') if item.get('data-partner') else None
        # hastickets = item.get('data-hastickets') if item.get('data-hastickets') else None

        data.append({
                "title": title.replace("'", "").replace('"', ''),
                "address": soup_adress,
                "category": category,
                "minprice": minprice,
                "url": url,
            })
        
    return data

def main():
    URL = "https://sxodim.com/almaty/places"
    url = URL
    all_data = []
    for page in range(1,119):
        if page >= 1:
            url = URL + f"?page={page}"
        HEADERS = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
        }
        html = get_html(url, HEADERS)
        data = processing(html)
        all_data.extend(data)
        print(f"Обработана страница {page}")

        
    for add_db in all_data:
        create_places(**add_db)
        
    return "Парсинг окончен"

print(main())