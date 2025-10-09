import json
from tokenize import endpats

import requests
from bs4 import BeautifulSoup

URL = "https://sports.uz/ru"
HOST = "http://sports.uz"
response = requests.get(URL)
# print(response.text)# getter
# print(response.json())
#404 Not found
#403 Forbidden Отказано в доступе
#401 Unauthorized Не авторизован
#400 Bad Request Плохой запрос

#200 всё работает
#201 Created
#204 NO CONTENT


html = response.text
soup = BeautifulSoup(html, "html.parser")
# news_block = soup.find("div", class_="news-list")
# news = news_block.find_all("div", class_="item")
# print(news)
# for i in news:
#     print(i.text)
def get_soup(link):
    response = requests.get(link)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return soup

def get_categorias():
    soup = get_soup(URL)
    navbar = soup.find("ul", class_="navbar-nav")
    categories = navbar.find_all("li", class_="nav-item")[2:]
    data = []
    for category in categories:
        if "dropdown-toggle" in category.find("a").get("class"):
            dropdown = category.find_all("a", class_="dropdown-item")
            print(dropdown)
            for item in dropdown:
                data.append({
                    "name": item.text.strip(),
                    "link": HOST + item.get("href")
                })
            continue

        link = HOST + category.find("a", class_="nav-link").get("href")
        data.append({
            "name": category.text,
            "link": link,
        })
    return data
get_categorias()

def get_articles(url):
    soup = get_soup(url)
    news_block = soup.find("div", class_="news-list")
    news = news_block.find_all("div", class_="item")
    articles = []
    for article in news:
        if "ads-item" in article.get("class"):
            continue
        title = article.find("h3").text
        description = article.find("p").text.strip()
        img = article.find("img", class_="lazy").get("data-src")
        link = article.find("a").get("href")
        print(link)
        articles.append({
            "title": title,
            "description": description,
            "img": img,
            "link": link,
        })
    return articles


def main():
    data = get_categorias()
    for category in data:
        print(category["link"])
        articles = category["name"], category["link"]
        category["articles"] = articles
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False, indent=4)
if __name__ == "__main__":
    main()

#
# for article in news:
#     if "ads-item" in article.get("class"):
#         continue
#     print(article.get("class"))
#     title = article.find("h3").text
#     description = article.find("p").text.strip()
#     img = article.find("img", class_="lazy").get("data-src")
#     link = article.find("a").get("href")
#     print(HOST+link)
#     print(description)
#     print(img)