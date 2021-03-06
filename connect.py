"""
Importing:
os for runing the clear command
json for read api responses
time for sleeping
requests for the actual rest client
yaml for rading the external config file
"""
import os
import json
import time
import requests
import yaml


# some CONSTS and VARS
yeslist = ["yes", "y"]
OPTIONS_DICTIONARY = {
    1: 'release_date',
    2: 'imdb_id',
    3: 'genres',
    4: 'overview',
    5: 'vote_average',
    6: 'all'
}


# Opening Config file. If not possible, the program exits
try:
    with open('config.yaml', encoding='UTF-8') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
except IOError:
    print("There was an error opening the config file")
    exit()

api_base_url = config['api_base_url']
api_version = config['API_VERSION']
api_key = config['API_KEY']


def clear_screen():
    """
    We clean the screen if the program starts over
    """
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')


def select_info():
    """
    Used for selecting what info do you want, after inputing the movie name or ID
    """
    possible_options = ["1 - Release date",
                        "2 - Its IMDB ID",
                        "3 - What is the genre",
                        "4 - An Overview of the story",
                        "5 - How is it rated",
                        "6 - All info you got!\n"]

    for option in possible_options:
        print(option)

    while True:
        selected_info = input("Select one option by its number\n")
        try:
            sel = int(selected_info)
            if sel < len(possible_options)+1:
                return sel
            else:
                print("Please, select an option between 1 and 6")
        except ValueError:
            print("Please, insert a number, not a text")


def query_by_id(endpoint):
    """
    To convert movie name to movie ID, which we actually use in the detailed info request
    """
    req_name = requests.get(endpoint)
    req_name_as_json = json.loads(req_name.text)
    results = req_name_as_json['results']
    for result in results:
        return result['id']


def main():
    """
    Actual program. It's inside a main function
    to make it easier to restart it at the end
    in case you select yes to the restart question
    """
    print("######################")
    print("###    Welcome.    ###")
    print("######################\n")
    print("I can tell you some info about any movie in the themoviedb.org website\n")

    print("Which method would you like to use to seach it?\nSelect an option:\n")
    while True:
        print("1 - By ID")
        print("2 - By Name")
        option = input()
        try:
            val = int(option)
            if val == 1:
                search_by = "ID"
                break
            elif val == 2:
                search_by = "Name"
                break
            print("Sorry, that is not a valid option")
        except ValueError:
            print("Please, insert a number, not a text")

    if search_by == "Name":
        movie_name = input("Input the movie name:\n")
        ep_path = "/search/movie"
        endpoint = f"{api_base_url}{api_version}{ep_path}?api_key={api_key}&query={movie_name}"
        movie_id = query_by_id(endpoint)
    else:
        while True:
            movie_id = input("Input the movie ID: ")
            try:
                val = int(movie_id)
                break
            except ValueError:
                print("Please, insert a number, not a text")

    ep_path = f"/movie/{movie_id}"
    endpoint = f"{api_base_url}{api_version}{ep_path}?api_key={api_key}"
    req_id = requests.get(endpoint)
    result_as_json = json.loads(req_id.text)

    if req_id.status_code != 200:
        restarting = "The program is restarting now"
        wait = 0
        print("\nThere was an error when making the request. The error was:")
        print("\"" + result_as_json['status_message'] + "\"\n\n")
        print(restarting)
        while wait < 5:
            time.sleep(0.3)
            print(wait*'.')
            wait = wait + 1
        clear_screen()
        main()
    else:
        if search_by == "ID":
            time.sleep(0.5)
            print("\nThe ID you chose belongs to the movie: \n" +
                  result_as_json['original_title'])
            time.sleep(2)

    print("\nWhat do you want to know about this movie?")
    selected = select_info()
    if selected != 6:
        print("\nHere is what I got about that:\n" +
              result_as_json[OPTIONS_DICTIONARY[selected]])
    else:
        print("Here is all info I got about the movie, in JSON format:\n" +
              json.dumps(result_as_json, indent=1))

    time.sleep(2)

    restart = input("\nDo you want to start again? (yes/y)\n").lower()
    if restart in yeslist:
        clear_screen()
        main()
    else:
        print("That was fun! Until the next time!.\nBye!")
        clear_screen()
        exit()


main()
