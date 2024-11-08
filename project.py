import csv
from datetime import datetime
import sqlite3
import requests
import random
import time
import os


# Connect to SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect('animes_data.db')
cursor = conn.cursor()

# MyAnimeList CLIENT_ID and search result LIMIT
CLIENT_ID = "4268486705dc98087214ea6c1f279480"
LIMIT = 5


# main function
def main():
    user_action = ""
    while user_action not in ["quit", "insert data", "get data"]:
        print("Enter (insert data) To Insert Data To Database (.db) file.")
        print("Enter (get data) To Get Data From Database (.db) file And Save It To (.csv) file.")
        print("Enter (quit) To Quit The Program.")
        time.sleep(1)
        print()
        user_action = input("What Do You Want To Do ? ").lower()
        print()

    # fetch data from myanimelist and insert it into .db file
    if user_action == "insert data":
        print("Note!! TXT File Must Contain 1 Anime Name In Line !")
        file_path = input("Enter File Path Or Name For (filename.txt) txt File: ")

        print()
        print("To Get The Exact Anime Name Result Enter (exact)")
        print("To Get All Result That Has Anime Name Enter (all)")
        print()
        global result_type
        result_type = input("What Type Of Result Do You Want To Get ? ").lower()
        print()

        if not file_path:
            return 1

        print()
        return process_txt_file(file_path)

    # get data from .db file and display it to .csv file
    elif user_action == "get data":
        cursor.execute(
            '''SELECT name FROM sqlite_master WHERE type='table' AND name=?''', ("animes",))
        if not cursor.fetchone():
            print("Database File is Empty, No Data To Get")
            print("Insert Data!!")
            return 2

        print("Enter One Format Only To Get It's Data From Database.")
        print("Format List [TV, OVA, Movie, Special, ONA, Music, CM, PV, TV Special]")
        print()
        print("Or Enter (all) To Get All From Database.")
        time.sleep(1)
        data_type = input("What Do You Want To Get ? ").lower()
        print()

        if not data_type:
            print("Enter Format Type! ")
            return 3

        try:
            current_date = str(datetime.now().strftime("%m-%d-%Y"))
            number = random.randint(1, 1000)
            global csv_name
            csv_name = f"animes-{number}_{current_date}"

            check_csv = get_animes_data(data_type)
            if check_csv == 0:
                print(f"CSV File With Name '{csv_name}' successfully Created.")
                conn.close()
                return 0

            elif check_csv == 1:
                print("Database File Table is Empty, No Data To Get!!")
                print("Insert Data!!")
                return 4

            else:
                print("Falied To Create CSV file! ")
                return 5

        except Exception as e:
            print(f"Error {e}")
            return 6


def process_txt_file(file_path: str):
    # Let The User Choose File Path For .txt file
    anime_list = read_txt_file(file_path)

    # Query the sqlite_master table to check if the table exists
    cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name=?''', ("animes",))

    # create database tables if not exist
    if not cursor.fetchone():
        create_tables()

    if not anime_list:
        print("Invalid TXT file.")
        return 1

    # prosses all animes in the file and insert it into database
    for anime_name in anime_list:
        print(f"Fetching data for {anime_name.title()}...")
        anime_data = fetch_anime_data(anime_name.lower())

        if result_type == "exact":
            print_if_anime_data(anime_name, anime_data)

        if anime_data == None:
            break
        time.sleep(2)  # Be polite to the API and avoid rate-limiting

    # Close the connection
    conn.close()
    return 0


def print_if_anime_data(anime_name, anime_data):
    # if there is data from API
    if anime_data and anime_data not in [1, 2]:
        print(f"Inserting Anime With Title '{anime_data['title']}'.")
        insert = insert_anime_data(anime_data)

        # print a massage if anime name in the database or inserted
        if insert == 1:
            print(f"Anime with title '{anime_data['title']}' already exists.")
            print()
        else:
            print(f"Inserted '{anime_data['title']}' into the database.")
            print()
    elif anime_data == 1:
        return 2

    elif anime_data == 2:
        print(f"Anime With Title '{anime_name}' Not Found.")
        print()
        return None

    else:
        return None


# make genres table if not exist in databas file
def create_tables(curs=None):
    # Create a table for storing genres
    cursor.execute('''CREATE TABLE IF NOT EXISTS animes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT UNIQUE,
                        alternative_titles TEXT,
                        mean INTEGER,
                        rank INTEGER,
                        popularity INTEGER,
                        num_list_users INTEGER,
                        num_scoring_users INTEGER,
                        status TEXT,
                        num_episodes INTEGER,
                        year INTEGER,
                        rating TEXT,
                        studios TEXT
                    )''')

    # Create a table for storing genres
    cursor.execute('''CREATE TABLE IF NOT EXISTS genres (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        anime_id INTEGER NOT NULL,
                        genre TEXT,
                        FOREIGN KEY(anime_id) REFERENCES animes(id)
                    )''')

    # Create a table for storing media type
    cursor.execute('''CREATE TABLE IF NOT EXISTS media_type (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        anime_id INTEGER NOT NULL,
                        type TEXT NOT NULL,
                        FOREIGN KEY(anime_id) REFERENCES animes(id)
                   )''')
    return 0


# Read anime names from txt file and make a list
def read_txt_file(file_path: str):
    try:
        with open(file_path, 'r') as file:
            anime_list = [line.strip() for line in file.readlines()]
        return anime_list

    except FileNotFoundError:
        return None


def fetch_anime_data(anime_name: str):
    # if anime name is too long
    if "," in anime_name and len(anime_name) > 62:
        name = anime_name.split(",", 1)[0]
        q = name.replace(" ", "%20")
    else:
        name = anime_name
        q = anime_name.replace(" ", "%20")

    # API endpoint with all fields included
    url = f"https://api.myanimelist.net/v2/anime?q={q}&limit={LIMIT}&fields=title,alternative_titles,mean,rank,popularity,num_list_users,num_scoring_users,media_type,status,genres,num_episodes,start_season,rating,studios"

    # Headers with your Client ID
    headers = {
        "X-MAL-CLIENT-ID": CLIENT_ID
    }

    # Send the GET request
    response = requests.get(url, headers=headers)

    # Print the search results (formatted as JSON)
    anime = response.json()

    try:
        for i in range(len(anime["data"])):
            title: str = anime["data"][i]["node"]['title']
            en: str = anime["data"][i]["node"]['alternative_titles']['en']

            if result_type == "exact":
                if anime_name == title.lower() or anime_name == en.lower():
                    return make_anime_data(anime, i)

                elif name in title.lower() or name in en.lower():
                    return make_anime_data(anime, i)

            elif result_type == "all":
                if anime_name in title.lower() or anime_name in en.lower():
                    anime_data = make_anime_data(anime, i)
                    print_if_anime_data(anime_name, anime_data)
                    insert_anime_data(anime_data)
            else:
                print("Enter 'Exact' Or 'All' To Choose Result Type")
                return 1
        return 0
    except KeyError:
        print(f"Error When Fetching '{anime_name.title()}'.")

        if anime["message"] == 'Invalid client id':
            print(f"Make Sure CLIENT_ID '{CLIENT_ID}' Is Right.")
            return None

        else:
            print("Check If Anime Name is Too Long.")
        print()
        return 2


def make_anime_data(anime: dict, i: int):
    # Prepare anime data
    try:
        anime_data = {
            'title': anime["data"][i]["node"]['title'],
            'alternative_titles': anime["data"][i]["node"]['alternative_titles']['en'],
            'mean': anime["data"][i]["node"]['mean'],
            'rank': anime["data"][i]["node"]['rank'],
            'popularity': anime["data"][i]["node"]['popularity'],
            'num_list_users': anime["data"][i]["node"]['num_list_users'],
            'num_scoring_users': anime["data"][i]["node"]['num_scoring_users'],
            'media_type': anime["data"][i]["node"]['media_type'],
            'status': anime["data"][i]["node"]['status'],
            'num_episodes': anime["data"][i]["node"]['num_episodes'],
            'year': anime["data"][i]["node"]['start_season']["year"],
            'rating': anime["data"][i]["node"]['rating'],
            'studios': anime["data"][i]["node"]['studios'][0]["name"],
            # list of genres
            'genres': [genre["name"] for genre in anime["data"][i]["node"]['genres']]
        }
        return anime_data

    except KeyError:
        anime_data = {
            'title': anime["data"][i]["node"]['title'],
            'alternative_titles': anime["data"][i]["node"]['alternative_titles']['en'],
            'mean': 0,
            'rank': 0,
            'popularity': anime["data"][i]["node"]['popularity'],
            'num_list_users': anime["data"][i]["node"]['num_list_users'],
            'num_scoring_users': anime["data"][i]["node"]['num_scoring_users'],
            'media_type': anime["data"][i]["node"]['media_type'],
            'status': anime["data"][i]["node"]['status'],
            'num_episodes': anime["data"][i]["node"]['num_episodes'],
            'year': 0,
            'rating': anime["data"][i]["node"]['rating'],
            'studios': "Unknown",
            # list of genres
            'genres': [genre["name"] for genre in anime["data"][i]["node"]['genres']]
        }
        return anime_data


# Insert anime data into the SQLite database
def insert_anime_data(anime_data: dict):
    # check if already exist
    cursor.execute('SELECT 1 FROM animes WHERE title = ?', (anime_data['title'],))

    if cursor.fetchone():
        return 1

    else:
        # Proceed with insertion
        cursor.execute('''INSERT INTO animes (title, alternative_titles, mean, rank, popularity, num_list_users, num_scoring_users, status, num_episodes, year, rating, studios)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            anime_data['title'],
            anime_data['alternative_titles'],
            anime_data['mean'],
            anime_data['rank'],
            anime_data['popularity'],
            anime_data['num_list_users'],
            anime_data['num_scoring_users'],
            anime_data['status'],
            anime_data['num_episodes'],
            anime_data['year'],
            anime_data['rating'],
            anime_data['studios']
        ))

        anime_id = cursor.lastrowid

        for genre in anime_data['genres']:
            cursor.execute('''INSERT INTO genres (anime_id, genre) VALUES (?, ?)''',
                           (anime_id, genre))

        cursor.execute('''INSERT INTO media_type (anime_id, type) VALUES (?, ?)''',
                       (anime_id, anime_data['media_type'],))
        conn.commit()
        return 0


def get_animes_data(data_type: str):
    # list of media types
    type_list = ['tv', 'ova', 'movie', 'special', 'ona', 'music', 'cm', 'pv', 'tv special']

    # check user input if in type_list
    if data_type in type_list:
        id_list = []
        for row in cursor.execute('SELECT anime_id FROM media_type WHERE type = ?', (data_type,)):
            id_list.append(row[0])

        if id_list:
            return make_csv_file(csv_name, id_list)
        else:
            return 1

    # if user want to get all metdia types
    elif data_type == "all":
        id_list = []
        for row in cursor.execute('SELECT anime_id FROM media_type'):
            id_list.append(row[0])

        if id_list:
            return make_csv_file(csv_name, id_list)
        else:
            return 1

    # if invalid format
    else:
        print("Invalid Format")
        return 2


def make_csv_file(csv_name: str, id_list: list):
    file_exists = os.path.isfile(f"{csv_name}.csv")
    if not file_exists:
        with open(f"{csv_name}.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "Title", "Alternative Titles", "Average Rating", "Rank",
                "Popularity", "Number of users who Listed", "Number Scoring Users",
                "Status", "Number Of Episodes", "Year", "Age rating", "Studios", "Format", "Genres"
            ])

    for id in id_list:
        for row in cursor.execute('SELECT * FROM animes WHERE id = ?', (id,)):
            with open(f"{csv_name}.csv", "a", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=[
                    "Title", "Alternative Titles", "Average Rating", "Rank",
                    "Popularity", "Number of users who Listed", "Number Scoring Users",
                    "Status", "Number Of Episodes", "Year", "Age rating", "Studios", "Format", "Genres"
                ])

                writer.writerow({
                    "Title": row[1],
                    "Alternative Titles": row[2],
                    "Average Rating": row[3],
                    "Rank": row[4],
                    "Popularity": row[5],
                    "Number of users who Listed": row[6],
                    "Number Scoring Users": row[7],
                    "Status": row[8],
                    "Number Of Episodes": row[9],
                    "Year": row[10],
                    "Age rating": row[11],
                    "Studios": row[12],
                    "Format": [i[0] for i in cursor.execute('SELECT type FROM media_type WHERE anime_id = ?', (id,))][0],
                    "Genres": ",".join([i[0] for i in cursor.execute('SELECT genre FROM genres WHERE anime_id = ?', (id,))])
                })
    return 0


if __name__ == "__main__":
    main()
