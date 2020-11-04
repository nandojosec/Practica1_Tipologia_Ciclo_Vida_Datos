import pandas as pd
import requests
from bs4 import BeautifulSoup

#GAME OF THRONES WEB SCRAPING

#Almacenar el sitio en una variable
url = 'http://www.imdb.com/title/tt0944947/episodes'

#Declarar los arreglos donde se guardarán los datos obtenidos
episodes = []
title = []
votes = []
ratings = []
dates = []

#Iteramos las temporadas de la serie (8 temporadas)
for season in range(1, 8):

    #Obtener las peticiones del sitio web por temporadas
    page = requests.get(url, params={'season': season})
    soup = BeautifulSoup(page.text, 'html.parser')
    pageEp = soup.find('div', class_='eplist')

    #Iterar por cada temporada para obtener los datos de cada episodio
    for epnro, div in enumerate(pageEp.find_all('div', recursive=False)):

        #Se obtiene los episodios de cada temporada y se agrega al arreglo
        episode = "{}.{}".format(season, epnro + 1)
        episodes.append(episode)

        #Se obtiene el título de los episodios y se agrega al arreglo
        titles_t = div.find(itemprop='name')
        titles = titles_t.get_text(strip=True)
        title.append(titles)

        #Se obtiene la votación de los episodios, se elimina los paréntesis,
        # la coma y finalmente se agrega al arreglo
        vote_v = div.find(class_='ipl-rating-star__total-votes')
        vote = vote_v.get_text(strip=True)
        vote = vote.lstrip('(')
        vote = vote.rstrip(')')
        vote = vote.replace(',', "")
        votes.append(vote)

        #Se obtiene el rating de los episodios y se agrega al arreglo
        rating_r = div.find(class_='ipl-rating-star__rating')
        rating = float(rating_r.get_text(strip=True))
        ratings.append(rating)

        #Se obtiene las fechas de estreno de los episodios y se agrega al arreglo
        date_f = div.find(class_='airdate')
        date = date_f.get_text(strip=True)
        dates.append(date)

#Se guarda los datos en un Data Frame
dframe = pd.DataFrame({'Episodio':episodes,'Titulo':title,'Votos':votes,'Rating':ratings,'F.Transmisión':dates})
print(dframe)

#Se exporta el Data Frame a un archivo excel y csv
dframe.to_excel('GameOfThrones.xlsx',index=False)
dframe.to_csv('Game_Of_Thrones.csv',index=False)
