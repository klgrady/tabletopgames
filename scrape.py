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
    for i in range (4,100):
        print("Starting on page", i)
        spider_go.parse_board(i)

if __name__ == "__main__":
    main()