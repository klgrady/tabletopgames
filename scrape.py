#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
#from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import re
from app.main import db, Games

load_dotenv('../../.env')

class TTGSpider():
    urls = {
        "board": 'https://boardgamegeek.com/browse/boardgame/page/',
        "rpg": "https://en.wikipedia.org/wiki/List_of_tabletop_role-playing_games",
        
    }
    
    def parse_rpg(self):
        html = requests.get(self.urls["rpg"])
        soup = BeautifulSoup(html.content, 'html.parser')
        results = soup.find_all("div", class_="div-col")
        for result in results:
            game_year = result.find("span", class_="mw-headline").text
            games_list = result.findAll("li")                           # for each game title within this year, get other info
            for title in games_list:
                desc_html = title.find("a", href=True)                  # get the link to the game's page
                go_next = requests.get('https://en.wikipedia.org' + desc_html.get('href'))
                dsoup = BeautifulSoup(go_next.content, 'html.parser')   # follow the description rabbit, Alice
                wrapper = dsoup.find("div", class_="mw-parser-output")
                description = wrapper.find("p", class_=None).text       # get <p> within div class=mw-parser-output
                title = title.text.replace("'", "''")                   # escape single quotes
                description = description.replace("'", "''").strip()    # escape single quotes
                description = re.sub(r"[\[\d+\]]", '', description)     # remove useless ref numbers
                data = {"name": title, "year": game_year, "desc": description, "type": 'RPG'}
                url = 'https://tabletopgames.herokuapp.com/v1/insert'
                response = requests.post(url=url, data=data)
                if response.status_code > 299:
                    print(f"Got {response.status_code} response from server on title")
                
        

    def parse_board(self, i):
        html = requests.get(self.urls["board"] + str(i))
        soup = BeautifulSoup(html.content, 'html.parser')
        results = soup.find_all(id="row_")
        for result in results:
            game_name = result.find("a", class_="primary")
            game_desc = result.find("p", class_="smallefont")
            game_year = result.find("span", class_="smallerfont")
            
            if game_year:
                game_yr = game_year.text.strip()
                year = re.search(r'\d{1,4}', game_yr).group(0)
            else:
                year = ""
            if game_desc:
                desc = game_desc.text.replace("'", "''")
            else:
                desc = ""

            name = game_name.text.replace("'", "''")
            try:
                with open('inserts.txt', 'a', encoding="utf-8") as f:
                    print(f"insert into games (name, year, description, type) values ('{name.strip()}', '{year}', '{desc.strip()}', 'board_game');", file=f)
                #self.cur.execute("insert into games (name, year, description, type) values (?, ?, ?, 'board game')", (game_name.text.strip(), year, game_desc.text.strip()))
            except Exception as e:
                print(f"Error inserting: {e}")

            

def main():
    spider_go = TTGSpider()
    #spider_go.dbc()
    # for i in range (4,100):
    #     print("Starting on page", i)
    #     spider_go.parse_board(i)
    spider_go.parse_rpg()

if __name__ == "__main__":
    main()