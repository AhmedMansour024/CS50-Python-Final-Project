# _Scrap Anime Details From MyAnimeList API_

## Video Demo for the Project:  [Watch Here](https://www.youtube.com/watch?v=tJAo1f6BAxI)

## Description:

Fetch Data From MyAnimeList API And Save it To db file And Extract Data From db File And Save it in CSV file Based on Format Type Like [TV, OVA, Movie, Special, ONA, Music, CM, PV, TV Special]

## Requirements For The Program to Run:
1. **You Must Have CLIENT ID From MyAnimeList Website.**
2. **You Have to Run (make) In The TERMINAL To install all necessary Libraries and to Create Environment for the program to run with no Error.**

###  CLIENT ID

You can apply for **CLIENT ID** at the [MyAnimeList Developer API](https://myanimelist.net/apiconfig).

### Run `make` to Set Up the Environment
```bash
make
```
## How to Use The Program ?
**The Program Has Two features**
1. **Insert Data:**
    - if the user want to insert data to the database file.
    - then the program will ask about the **result type** Meaning:
        - if the user want to get the result extractly the same as the txt, Enter **exact.**
        - if the user want all result that Has **txt name** in it, Enter **all.**

    - after that user will enter his **CLIENT ID**, then the program will **start** fetching for all the anime in the **txt file** And Save it to the **db file**.

2. **Get Data**
    - if the user want to extract data from the database file by creating **CSV file.**
    - then the program will ask about **Format type** And There is Two Choices:
        - if user want one format only Like [**TV**, **OVA**, **Movie**, **Special**, **ONA**, **Music**, **CM**, **PV**, **TV Special**].
        - if the user want to get all formats **all**.
