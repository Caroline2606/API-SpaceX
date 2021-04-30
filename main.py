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
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
        raise SpacexTimeout('The request timeout.')
    return response.json()


data = fetch_spacex_data('https://api.spacexdata.com/v3/launches')

flights = []
for row in response.json():
    flight_number = row.get('flight_number', None)
    mission_name = row.get('mission_name', None)
    rocket_id = row.get('rocket_id', None)
    launch_date_utc = row.get('launch_date_utc', None)
    video_link = row.get('video_link', None)
    flights.append([flight_number, mission_name, rocket_id, launch_date_utc, video_link])

with open("space.csv", 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['flight_number', 'mission_name', 'rocket_id', 'launch_date_utc', 'video_link'])
    csvwriter.writerows(flights)

print(flights)
