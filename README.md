    # Scrap Anime Details From MyAnimeList API
    #### Video Demo:  <https://www.youtube.com/watch?v=tJAo1f6BAxI>
    #### Description:
    First CLIENT ID:
    Before Running The Program, User Need To Have CLIENT ID From MyAnimeList Website.
    You Can Apply For One at MyAnimeList Website.

    Second running make:
    if you are running the program on Codespace: Like CS50 or on a Device Like Pc.
    you need to run (make) to install all necessary Libraries for the program and to make Environment for the program to run with no Error.

    if you can not run make that means you need to install make.

    Third What the Program will do?
    the program will do two things:
    1- use MyAnimeList API to fetch Anime Data by using CLIENT ID and txt file containing 1 anime a line and save this data to database file.
    2- extract the data in the database file and save it to csv file.

    Forth running the program:
    after running, the user will be asked about what you want to do?
    if the user want to insert data to the database file, Enter (insert data).
    insert data:
    then the program will ask about the result type.
    if the user want the result extractly the same as the txt, Enter (exact).
    if the user want all result, meaning every anime that has then name from txt file in it, Enter (all).

    after that user will enter his CLIENT ID from MyAnimeList.
    then the program will start fetching for all the anime in the txt file.

    if the user want to create csv file and extract data from the database file, Enter (get data).
    get data:
    then the program will ask about Format type Like [TV, OVA, Movie, Special, ONA, Music, CM, PV, TV Special]
    if the user want to get that format only.
    and if the user want to get all formats, Enter (all).

    Fifth What the program Functions?
    main Function and 9 more Functions.

    1- main function:
    is the main function that runs the program and calls all other functions.

    2- process_txt_file function:
    is the main function that calls every function needed to use (insert data) feature.

        it calls:
        1- read_txt_file function: that is validate the txt file if it exist and create a list of all anime names in the txt file.

        2- create_tables function to create all the necessary tables if not exist.

        3- fetch_anime_data function fetch the anime data from MyAnimeList API and change the response to json and based on the user result type selection (exact, all) the function will call:
            1- if result type = exact :
            calls make_anime_data function that make a dictionary to make inserting data to the database file easier.

            2- if result type = all :
            calls make_anime_data function that make a dictionary to make inserting data to the database file easier.
            then calls print_if_anime_data function that print to the user what anime name is processing.
            then calls insert_anime_data function to insert fetched data to the database file.

    3- make_anime_data function:
    is called when user choose to use (get data) feature.
        1- it checks if the database file exist and has all necessary tables.
        2- get all data based on the user Format type [TV, OVA, Movie, Special, ONA, Music, CM, PV, TV Special] or if the user choose to get all formats and enter all.
        3- calls make_csv_file function and create a csv containing all data.
