import json
import requests
from datetime import datetime, timedelta

url = "https://nistaldykorgan.edupage.org/timetable/server/currenttt.js?__func=curentttGetData"
classid = "-140"

def request_tt(classid = classid):
    # Get the current date
    current_date = datetime.now()
    # Calculate the start of the current week (usually Sunday)
    start_of_week = current_date - timedelta(days=current_date.weekday())
    # Calculate the end of the current week (usually Saturday)
    end_of_week = start_of_week + timedelta(days=6)
    # Format the results as strings in the "datefrom" and "dateto" format
    start_of_week_str = start_of_week.strftime("%Y-%m-%d")
    end_of_week_str = end_of_week.strftime("%Y-%m-%d")

    headers = {
        "Content-Type": "text/plain",
        "Content-Length": "0",
        "User-Agent": "PostmanRuntime/7.33.0",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cookie": "PHPSESSID=e645fe0824df28dff6798f7df59c406f",
        "Host": "nistaldykorgan.edupage.org"
    }
    payload = {
        "__args": [
            None,
            {
                "year": 2023,
                "datefrom": start_of_week_str,
                "dateto": end_of_week_str,
                "table": "classes",  # needed table name
                "id": classid,  # needed class id(fetched from db)
                "showColors": True,  # Responcible for colors
                "showIgroupsInClasses": False,  # idk what it does
                "showOrig": True,  # is responsible for the “Canceled” parameter, I don’t know what it means
                "log_module": "CurrentTTView",  # nvm

            }
        ],
        "__gsh": "00000000"
    }

    response = requests.post(url=url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        data = response.json()
        # print(json.dumps(data, indent=4))
        with open(f"data/{classid}.json","w") as file:
            file.write(json.dumps(data, indent=4))

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

if __name__ == "__main__":
    request_tt()
