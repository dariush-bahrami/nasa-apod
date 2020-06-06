import json
import requests
from pathlib import Path
import pprint as pp
import os

with open("api_data.json", "r") as open_file:
    api_data = json.load(open_file)

api_key = api_data['key']

apod_url = "https://api.nasa.gov/planetary/apod"

# date = '2020-01-22'

request_parameters = {
    'api_key': api_key,
    # 'date':date,
    'hd': 'True'
}

response = requests.get(apod_url, params=request_parameters).json()
pp.pprint(response)
hd_image = requests.get(response['hdurl'])

database_location = Path('astronomy_pictures')
today_folder = Path(' '.join([response['date'], response['title']]))
txt_file_name = Path(' '.join([response['title'], '.txt']))
picture_format = '.jpg'
picture_file_name = Path(' '.join([response['title'], picture_format]))

txt_file_path = Path.joinpath(database_location, today_folder, txt_file_name)
picture_file_path = Path.joinpath(database_location, today_folder,
                                  picture_file_name)

database_path = Path(database_location)
if not database_path.is_dir():
    os.mkdir(database_path)

today_folder_path = Path.joinpath(database_location, today_folder)
if not today_folder_path.is_dir():
    os.mkdir(today_folder_path)
   

with open(txt_file_path, mode='w') as stream:
    stream.write(response['explanation'])

with open(picture_file_path, mode='wb') as stream:
    stream.write(hd_image.content)