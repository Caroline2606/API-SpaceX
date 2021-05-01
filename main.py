import requests
import csv

url = 'https://api.spacexdata.com/v3/launches'
response = requests.get(url)



class SpacexHttpError(Exception):
    pass


class SpacexURLRequired(Exception):
    pass


class SpacexTimeout(Exception):
    pass


def fetch_spacex_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
        raise SpacexHttpError('Fail to fetch SpaceX data.')
    except requests.exceptions.URLRequired:
        raise SpacexURLRequired('A valid URL is required to make a request.')
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
        raise SpacexTimeout('The request timeout.')

    return response.json()


data = fetch_spacex_data('https://api.spacexdata.com/v3/launches')


flights = []
for row in data:
    flight_number = row['flight_number']
    mission_name = row['mission_name']
    rocket_id = row['rocket']['rocket_id']
    launch_date_utc = row['launch_date_utc']
    video_link = row['links']['video_link']
    flights.append([flight_number, mission_name, rocket_id, launch_date_utc, video_link])

with open("space.csv", 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['flight_number', 'mission_name', 'rocket_id', 'launch_date_utc', 'video_link'])
    csvwriter.writerows(flights)

print(flights)
