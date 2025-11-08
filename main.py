import json
import requests
from bs4 import BeautifulSoup

URL = "https://sports.uz/ru"
HOST = "http://sports.uz"
response = requests.get(URL)



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
        link_tag = category.find("a")
        if not link_tag:
            continue
        if "dropdown-toggle" in link_tag.get("class", []):
            dropdown = category.find_all("a", class_="dropdown-item")
            for item in dropdown:
                data.append({
                    "name": item.text.strip(),
                    "link": HOST + item.get("href")
                })
            continue
        data.append({
            "name": link_tag.text.strip(),
            "link": HOST + link_tag.get("href")
        })
    return data

def get_articles(url):
    soup = get_soup(url)
    news_block = soup.find("div", class_="news-list")
    if not news_block:
        return []
    news = news_block.find_all("div", class_="item")
    articles = []
    for article in news:
        if "ads-item" in article.get("class", []):
            continue
        title_tag = article.find("h3")
        desc_tag = article.find("p")
        img_tag = article.find("img", class_="lazy")
        link_tag = article.find("a")
        if not title_tag or not link_tag:
            continue
        articles.append({
            "title": title_tag.text.strip(),
            "description": desc_tag.text.strip() if desc_tag else "",
            "img": img_tag.get("data-src") if img_tag else "",
            "link": HOST + link_tag.get("href")
        })
    return articles

def get_all_articles():
    data = get_categorias()
    all_data = []
    for category in data:
        print(f"\n{category['name']}\n{category['link']}\n")
        articles = get_articles(category["link"])
        for i, a in enumerate(articles, 1):
            print(f"{i}. {a['title']}\n{a['description']}\n{a['img']}\n{a['link']}\n")
        all_data.append({
            "category": category["name"],
            "link": category["link"],
            "articles": articles
        })
    return all_data

def main():
    data = get_all_articles()
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()



# print(response.text)# getter
# print(response.json())
#404 Not found
#403 Forbidden Отказано в доступе
#401 Unauthorized Не авторизован
#400 Bad Request Плохой запрос

#200 всё работает
#201 Created
#204 NO CONTENT
#
#
# html = response.text
# soup = BeautifulSoup(html, "html.parser")
# # news_block = soup.find("div", class_="news-list")
# # news = news_block.find_all("div", class_="item")
# # print(news)
# # for i in news:
# #     print(i.text)
# def get_soup(link):
#     response = requests.get(link)
#     html = response.text
#     soup = BeautifulSoup(html, "html.parser")
#     return soup
#
# def get_categorias():
#     soup = get_soup(URL)
#     navbar = soup.find("ul", class_="navbar-nav")
#     categories = navbar.find_all("li", class_="nav-item")[2:]
#     data = []
#     for category in categories:
#         if "dropdown-toggle" in category.find("a").get("class"):
#             dropdown = category.find_all("a", class_="dropdown-item")
#             print(dropdown)
#             for item in dropdown:
#                 data.append({
#                     "name": item.text.strip(),
#                     "link": HOST + item.get("href")
#                 })
#             continue
#
#         link = HOST + category.find("a", class_="nav-link").get("href")
#         data.append({
#             "name": category.text,
#             "link": link,
#         })
#     return data
# get_categorias()
#
# def get_articles(url):
#     soup = get_soup(url)
#     news_block = soup.find("div", class_="news-list")
#     news = news_block.find_all("div", class_="item")
#     articles = []
#     for article in news:
#         if "ads-item" in article.get("class"):
#             continue
#         title = article.find("h3").text
#         description = article.find("p").text.strip()
#         img = article.find("img", class_="lazy").get("data-src")
#         link = article.find("a").get("href")
#         print(link)
#         articles.append({
#             "title": title,
#             "description": description,
#             "img": img,
#             "link": link,
#         })
#     return articles
#
#
# def main():
#     data = get_categorias()
#     for category in data:
#         print(category["link"])
#         articles = category["name"], category["link"]
#         category["articles"] = articles
#     with open("data.json", "w", encoding="utf-8") as f:
#         json.dump(data,f,ensure_ascii=False, indent=4)
# if __name__ == "__main__":
#     main()
#
# #
# # for article in news:
# #     if "ads-item" in article.get("class"):
# #         continue
# #     print(article.get("class"))
# #     title = article.find("h3").text
# #     description = article.find("p").text.strip()
# #     img = article.find("img", class_="lazy").get("data-src")
# #     link = article.find("a").get("href")
# #     print(HOST+link)
# #     print(description)
# #     print(img)