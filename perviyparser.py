import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# это чтоб меня не кикнули с сайта
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
}

def hh_rabota():
    url = "https://hh.kz/search/vacancy?text=Data+Scientist&area=40"
    
    print("братишка подожди ка")
    try:
        zapros = requests.get(url, headers=HEADERS, timeout=10)
        if zapros.status_code != 200:
            print(f"сибался. потому что: {zapros.status_code}")
            return []
    except Exception as e:
        print(f"жилки нету у меня : {e}")
        return []

    soup = BeautifulSoup(zapros.text, 'html.parser')
    
    vakansyy = soup.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})
    if not vakansyy:
        vakansyy = soup.find_all('div', class_='vacancy-card--container')
    data = []
    for v in vakansyy:
        title_tag = v.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        if not title_tag:
            title_tag = v.find('span', {'data-qa': 'serp-item__title-text'})
            if title_tag:
                link_tag = v.find('a')
                link = link_tag['href'] if link_tag else ""
            else:
                continue
        else:
            link = title_tag.get('href', '')
        
        title = title_tag.text.strip()
        
        snippet_text = ""
        snippet_elements = v.find_all(['div', 'span'], {'data-qa': ['vacancy-serp__vacancy_snippet_responsibility', 'vacancy-serp__vacancy_snippet_requirement']})
        for elem in snippet_elements:
            snippet_text += " " + elem.text.lower()
            
        if not snippet_text:
            snippet_text = v.text.lower()
        
        techs = []
        if "python" in snippet_text: techs.append("Python")
        if "sql" in snippet_text: techs.append("SQL")
        if "tableau" in snippet_text: techs.append("Tableau")
        
        data.append({
            "название вакансии": title,
            "технологии": ", ".join(techs) if techs else "не указан",
            "ссылкагой": link
        })
    
    return data
if __name__ == "__main__":
    results = hh_rabota()
    if results:
        df = pd.DataFrame(results)
        df.to_excel("hh_vakansyy.xlsx", index=False)
        print(f"НАШЕЕЛЛ ШШС: {len(results)}")
        print("Файл 'hh_vakansyy.xlsx' он создался радуйся братишка")
    else:
        print("кароче братишка брысь отсюда")