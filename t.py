import requests
import cloudscraper
from bs4 import BeautifulSoup
import random
import time

def generate(selected):
    url = "https://www.albumoftheyear.org"
    scraper = cloudscraper.create_scraper()
    decade = 'all'
    genres = ['6-highest-rated', '2-alternative-rock', '34-ambient', '62-black-metal', '143-classical',
              '507-contemporary-folk', '132-dance', '6-electronic', '263-edm', '9-experimental', '5-folk',
              '49-hardcore-punk', '3-hip-hop', '4-indie-pop', '1-indie-rock', '35-jazz', '40-metal', '15-pop',
              '103-pop-rock', '28-punk', '22-r-and-b', '7-rock', '213-trap-rap', '26-shoegaze', '366-mandopop']
    while True:
        try:
            a = [genres[int(i)] for i in selected]
            genre = a[random.randint(0,len(a)-1)]
            url = f'{url}/genre/{genre}/all' if genre != genres[0] else f'{url}/ratings/{genre}/all/1'
            def get_soup(url):
                headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.albumoftheyear.org/',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Connection': 'keep-alive',
                }
                session = requests.Session()
                session.headers.update(headers)
                response = scraper.get(url)
                return BeautifulSoup(response.text, "html.parser")
            soup = get_soup(url)
            pages = soup.find('div', class_ = "pageSelectRow").find_all()[-1].text
            break
        except:
            time.sleep(2)
    time.sleep(2)

    while True:
        try:
            page = random.randint(1, int(pages))
            album = random.randint(1,25)
            url = f'https://www.albumoftheyear.org/genre/{genre}/all/{page}' if genre != genres[0] else f'https://www.albumoftheyear.org/ratings/{genre}/all/{page}'
            soup2 = get_soup(url)
            pick = soup2.find('div', class_ = 'wideLeft alignTop').find_all('div', class_= 'albumListRow')[album-1]
            name = pick.find('h2', class_ = 'albumListTitle').find('a').text
            cover = pick.find('div', class_= 'albumListCover').find('a').find('img').get('data-src')
            date = pick.find('div', class_= 'albumListDate').text
            genres = pick.find('div', class_= 'albumListGenre').text
            links = pick.find('div', class_ = 'albumListLinks').find_all('a')
            am = links[1].get('href')
            spotify = links[2].get('href')
            print( name, cover, date, genres, am, spotify)
            return {"name": name, "cover": cover, "date": date, "genres": genres, "am": am, "spotify": spotify}

        except:
            time.sleep(2)
