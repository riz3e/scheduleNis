import json
from datetime import datetime, timedelta

import requests

import classesdb
import classroomsdb
import periodsdb
import subjectsdb
import teachersdb

# Get the current date
current_date = datetime.now()
# Calculate the start of the current week (usually Sunday)
start_of_week = current_date - timedelta(days=current_date.weekday())
# Calculate the end of the current week (usually Saturday)
end_of_week = start_of_week + timedelta(days=6)
# Format the results as strings in the "datefrom" and "dateto" format
start_of_week_str = start_of_week.strftime("%Y-%m-%d")
end_of_week_str = end_of_week.strftime("%Y-%m-%d")
querystring = {"__func": "mainDBIAccessor"}
payload = {
    "__args": [
        None,
        2023,
        {"vt_filter": {
            "datefrom": start_of_week_str,
            "dateto": end_of_week_str
        }},
        {
            "op": "fetch",
            "needed_part": {
                "teachers": ["short", "name", "firstname", "lastname", "subname", "code", "cb_hidden", "expired",
                             "firstname", "lastname", "short"],
                "classes": ["short", "name", "firstname", "lastname", "subname", "code", "classroomid"],
                "classrooms": ["short", "name", "firstname", "lastname", "subname", "code", "name", "short"],
                "igroups": ["short", "name", "firstname", "lastname", "subname", "code"],
                "students": ["short", "name", "firstname", "lastname", "subname", "code", "classid"],
                "subjects": ["short", "name", "firstname", "lastname", "subname", "code", "name", "short"],
                "events": ["typ", "name"],
                "event_types": ["name", "icon"],
                "subst_absents": ["date", "absent_typeid", "groupname"],
                "periods": ["short", "name", "firstname", "lastname", "subname", "code", "period", "starttime",
                            "endtime"],
                "dayparts": ["starttime", "endtime"],
                "dates": ["tt_num", "tt_day"]
            },
            "needed_combos": {}
        }
    ],
    "__gsh": "00000000"
}
headers = {
    "authority": "nistaldykorgan.edupage.org",
    "accept": "*/*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json; charset=UTF-8",
    "cookie": "PHPSESSID=e645fe0824df28dff6798f7df59c406f",
    "origin": "https://nistaldykorgan.edupage.org",
    "referer": "https://nistaldykorgan.edupage.org/",
    "sec-ch-ua": '"Opera";v="103", "Not;A=Brand";v="8", "Chromium";v="117"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0"
}

response = requests.request("POST", "https://nistaldykorgan.edupage.org/rpr/server/maindbi.js", json=payload,
                            headers=headers, params=querystring)

maindb_path = "data/maindbi.json"

teachersdb.convertJsonToDB(path=maindb_path)
subjectsdb.convertJsonToDB(path=maindb_path)
periodsdb.convertJsonToDB(path=maindb_path)
classroomsdb.convertJsonToDB(path=maindb_path)
classesdb.convertJsonToDB(path=maindb_path)

# with open("data/maindbi.json", "r", encoding='utf-8') as file:
#     if(json.loads(response.text) == json.loads(file.read())): print(True)

with open("data/maindbi.json", "w", encoding='utf-8') as file:
    file.write(json.dumps(json.loads(response.text), ensure_ascii=False, indent=4))