from bs4 import BeautifulSoup as bs4
import requests

resposne = requests.get("https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/")


soup = bs4(resposne.text,"html.parser")

h3 = soup.find_all(name="h3",class_="title")

with open("dayten/scrapping/mv.txt","w+",encoding='utf-8') as write_file:
    for h in reversed(h3):
        write_file.write(h.getText() + "\n")