import requests
import csv

response = requests.get('https://api.spacexdata.com/v3/launches')
data = response.json()

class SpacexHttpError(Exception):
    pass


class SpacexURLRequired(Exception):
    pass


class SpacexTimeout(Exception):
    pass


def fetch_spacex_data(url):
    try:
        response = requests.get('https://api.spacexdata.com/v3/launches')
        response.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
        raise SpacexHttpError('Fail to fetch SpaceX data.')
    except requests.exceptions.URLRequired:
        raise SpacexURLRequired('A valid URL is required to make a request.')

    return response.json()


data = fetch_spacex_data('https://api.spacexdata.com/v3/launches')


flights = []
for row in response.json():
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
