import requests
import base64
import json
import os,sys
from time import sleep
from datetime import datetime,timedelta

ACCESS_TOKEN = "YOUR_TOKEN"
BASE_URL = "https://api.zoom.us/v2/"

HEADERS = {
    'authorization': f"Bearer {ACCESS_TOKEN}",
    'content-type': "application/json"
}

def make_request(url, headers):
    r = requests.get(url, headers=headers)
    r_json = r.json()
    return r_json

def get_user_list():
    users_list_endpoint = BASE_URL + f"users?status=active&page_size=30&page_number=1"
    users_data = make_request(users_list_endpoint, HEADERS)
    page_count = users_data['page_count']
    users_list = []
    for i in range(1, page_count+1):
        users_list_endpoint = BASE_URL + f"users?status=active&page_size=30&page_number={i}"
        users_data = make_request(users_list_endpoint, HEADERS)
        for user in users_data["users"]:
            users_list.append(user)
    return users_list

def format_string_datetime(value):
    datetime_dt = datetime.strptime(value,'%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=3)
    datetime_dt_str = datetime_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    datetime_str = datetime_dt_str.replace("T", ":").replace("Z", "")
    return datetime_str,datetime_dt

def main(users_list):
    for user in users_list:
        user_id = user["id"]
        user_email = user["email"]
        user_name = user["first_name"] + "-" + user["last_name"]
        recordings_url = BASE_URL + f"users/{user_id}/recordings"
        recordings_data = make_request(recordings_url, HEADERS)
        curr_user_meetings = recordings_data["meetings"]

        if curr_user_meetings:
            for meeting in curr_user_meetings:
                curr_user_recordings = meeting['recording_files']
                curr_user_recordings_count = meeting['recording_count']
                curr_user_recordings_datetime_str, curr_user_recordings_datetime_dt = format_string_datetime(meeting['start_time'])
                curr_user_recordings_topic = meeting['topic']
                folder_name = "./" + user_name + '/' + curr_user_recordings_datetime_str
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                else:
                    continue
                if curr_user_recordings:
                    print (f'\n{curr_user_recordings_count} Recordings found for User {user_name}; Downloading recording files\n')
                    for recording in curr_user_recordings:
                        file_name = curr_user_recordings_topic + recording['recording_type'] + '.' + recording['file_type']
                        path_to_video = folder_name + "/" + file_name
                        if not os.path.exists(path_to_video):
                            recording_files_data_download_url = recording["download_url"] + "/?access_token=%s"%ACCESS_TOKEN
                            print ("Downloading %s" % file_name)
                            r = requests.get(recording_files_data_download_url)
                            total_size = int(r.headers.get('content-length', 0))
                            block_size = 32 * 1024  # 32 Kibibytes
                            with open(path_to_video, "wb") as f:
                                progress_bar_length = 0
                                for data in r.iter_content(block_size):
                                    progress_bar_length += len(data)
                                    f.write(data)
                                    per = (100.0 * progress_bar_length) / total_size
                                    done = int(50 * progress_bar_length / total_size)
                                    sys.stdout.write("\r[%s%s]%f%%" % ('=' * done, ' ' * (50-done),per))
                                    sys.stdout.flush()
                                    print (f"\nFinished Downloading {file_name}\n")
                        else:
                            continue
                else:
                    continue
        else:
            continue

if __name__ == "__main__":
    users_list = get_user_list()
    main(users_list)



