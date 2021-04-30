import requests
import csv

response = requests.get('https://api.spacexdata.com/v3/launches')
data = response.json()


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
