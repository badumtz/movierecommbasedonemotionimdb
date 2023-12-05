from bs4 import BeautifulSoup as SOUP
import requests as HTTP
import json

def main(emotion):
    url_mapping = {
        "Sadness": 'http://www.imdb.com/search/title?genres=drama&title_type=feature&sort=moviemeter,asc',
        "Disgust": 'http://www.imdb.com/search/title?genres=musical&title_type=feature&sort=moviemeter,asc',
        "Angerness": 'http://www.imdb.com/search/title?genres=family&title_type=feature&sort=moviemeter,asc',
        "Anticipation": 'http://www.imdb.com/search/title?genres=thriller&title_type=feature&sort=moviemeter,asc',
        "Fearness": 'http://www.imdb.com/search/title?genres=sport&title_type=feature&sort=moviemeter,asc',
        "Enjoyment": 'http://www.imdb.com/search/title?genres=thriller&title_type=feature&sort=moviemeter,asc',
        "Trust": 'http://www.imdb.com/search/title?genres=western&title_type=feature&sort=moviemeter,asc',
        "Surpriseness": 'http://www.imdb.com/search/title?genres=film_noir&title_type=feature&sort=moviemeter,asc'
    }

    urlhere = url_mapping.get(emotion, '')
    if not urlhere:
        print(f"Invalid emotion: {emotion}. Please choose a valid emotion.")
        return None

    response = HTTP.get(urlhere)
    data = response.text

    # Find the JSON data embedded in the HTML
    start = data.find("IMDbReactWidgets")
    end = data.find("};", start) + 1

    # Check if the start and end indices are valid
    if start == -1 or end == -1:
        print("Failed to extract data.")
        return None

    json_data_str = data[start:end].split("IMDbReactWidgets.init(")[1]
    json_data_str = json_data_str.replace("'", "\"")  # Convert single quotes to double quotes
    try:
        json_data = json.loads(json_data_str)
        movie_list = json_data["titles"]
    except (json.JSONDecodeError, KeyError):
        print("Failed to extract data.")
        return None

    return movie_list

if __name__ == '__main__':
    emotion = input("What emotion are you feeling: ")
    movie_list = main(emotion)

    if movie_list is not None:
        for movie in movie_list:
            title = movie.get("title", "")
            print(title)
