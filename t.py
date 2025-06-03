import requests
import cloudscraper
from bs4 import BeautifulSoup
import random
import time
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import os
from urllib.parse import quote_plus
import math
from flask import session
def get_soup(url):
        scraper = cloudscraper.create_scraper()
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
def generate(selected):
    url = "https://www.albumoftheyear.org"
    genres = ['6-highest-rated', '2-alternative-rock', '34-ambient', '62-black-metal', '143-classical',
              '507-contemporary-folk', '132-dance', '6-electronic', '263-edm', '9-experimental', '5-folk',
              '49-hardcore-punk', '3-hip-hop', '4-indie-pop', '1-indie-rock', '35-jazz', '40-metal', '15-pop',
              '103-pop-rock', '28-punk', '22-r-and-b', '7-rock', '213-trap-rap', '26-shoegaze']
    while True:
        try:
            a = [genres[int(i)] for i in selected]
            genre = a[random.randint(0,len(a)-1)]
            url = f'{url}/genre/{genre}/all' if genre != genres[0] else f'{url}/ratings/{genre}/all/1'
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

def find_similiar(spotify):
    token_info = session.get("token_info")
    if not token_info:
        return False

    sp = spotipy.Spotify(auth=token_info["access_token"])
    try:
        album = sp.album(spotify)
    except:
         return False
    name = album['name']
    artist = album['artists'][0]['name']
    print(name,artist)
    query = quote_plus(name)
    print(query)
    url = f"https://www.albumoftheyear.org/search/?q={query}"
    print(url)
    search = get_soup(url)
    results = search.find_all('div', class_='albumBlock')
    aoty_link = None
    for result in results:
         artist_name = result.find_all('a')[1].find('div').text
         album_name = result.find_all('a')[2].find('div').text
         print(name, album_name)
         print(artist, artist_name)
         type = result.find('div', class_ = 'type').text
         if name.lower() == album_name.lower() and artist.lower() == artist_name.lower():
              aoty_link = f'https://www.albumoftheyear.org{result.find_all('a')[0].get('href')}'
              print(aoty_link)
              break
    if not aoty_link:
        return False
    time.sleep(1)

    genres = get_genres(aoty_link=aoty_link)
    print(genres)
    genre = genres[random.randint(0,len(genres)-1)]
    time.sleep(1.3)
    genre_link = f'https://www.albumoftheyear.org{genre}/all'
    soup2 = get_soup(genre_link)
    pages = soup2.find('div', class_ = "pageSelectRow").find_all()[-1].text
    page = random.randint(1, int(pages))
    albums = soup2.find('div', class_ = 'wideLeft alignTop').find_all('div', class_ = 'albumListRow')
    compiled = []
    for album in albums:
        a_genres = [x.get('href') for x in album.find('div', class_ = 'albumListGenre').find_all('a')]
        similiarity = jaccard_similarity(genres, a_genres)
        compiled.append({str(album.get('id')): similiarity})
    items = [list(d.keys())[0] for d in compiled]
    similarities = [list(d.values())[0] for d in compiled]
    weights = [math.exp(s * 7) for s in similarities]
    selected = random.choices(items, weights=weights, k=1)[0]
    pick = soup2.find('div', class_ = 'wideLeft alignTop').find('div', id= selected)
    name = pick.find('h2', class_ = 'albumListTitle').find('a').text
    
    date = pick.find('div', class_= 'albumListDate').text
    genres = pick.find('div', class_= 'albumListGenre').text
    links = pick.find('div', class_ = 'albumListLinks').find_all('a')
    am = links[1].get('href')
    spotify = links[2].get('href')
    try:
        cover = pick.find('div', class_= 'albumListCover').find('a').find('img').get('data-src')
    except:
        cover = sp.album(spotify)['images']['url']
    return {"name": name, "cover": cover, "date": date, "genres": genres, "am": am, "spotify": spotify}   
def get_genres(aoty_link):
    soup = get_soup(aoty_link)
    genres = [x.get('href') for x in soup.find_all('div', class_ = 'detailRow')[3].find_all('a')]
    return genres

def jaccard_similarity(list1, list2):
    set1, set2 = set(list1), set(list2)
    intersection = set1 & set2
    union = set1 | set2
    return len(intersection) / len(union)
