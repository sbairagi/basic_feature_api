# from .models import StocksTips
import requests
from bs4 import BeautifulSoup
# from django.db.models import Q



def update_Stocktips():
    url = "https://www.bhaskar.com/local/mp/mandsaur/"
    r = requests.get(url)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    stockstips = soup.find_all('div', class_="ba1e62a6")
    
    for i in stockstips:
        # published_On = i.findAll('p')[0].text[13:]
        # p1 = i.findAll('li')[1].text
        desc = i.findChild('h3').text
        title = i.findChild('span').text
        image_url = i.findChild('img')['src']
        # full_blog_url = i.find('a')['href']
        full_blog_url = i.find('li', class_="c7ff6507").findChild("a")['href']
        # print(adfdf, "jvhv")
        full_blog_url = "https://www.bhaskar.com" + full_blog_url
        # print(full_blog_url, i)
        video_path =full_blog_url.replace('/news/', '/video/')
        
        r = requests.get(full_blog_url)
        htmlContent = r.content
        soup = BeautifulSoup(htmlContent, 'html.parser')
        full_blog = soup.find('div', class_="bf64dc76")
        description_p = full_blog.findChildren('p')
        description = ""
        # print("xfgx", description_p)
        for j in description_p:
            description = description + "\n" + j.text
            # print("hgjgj", j.text)
        print("vgh:", description, video_path)
        

update_Stocktips()