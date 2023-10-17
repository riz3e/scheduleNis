import json
import requests
from datetime import datetime, timedelta

import classesdb
import classroomsdb
import subjectsdb
import teachersdb

classid = "-140"


# class ttday():
#     # date, uniperiod, starttime, endtime, subjectid, classids, groupnames,
#     # teacherid, colors, classroomids, durationperiods, cellSlices, cellOrder
#     def __init__(self):
#


def request_tt(classid=classid):
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

    response = requests.post(
        url="https://nistaldykorgan.edupage.org/timetable/server/currenttt.js?__func=curentttGetData",
        data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        data = response.json()["r"]['ttitems']

        print("data fetched")
        with open(f"data/{classid}.json", "w", encoding='utf-8') as file:
            file.write(json.dumps(data, indent=4, ensure_ascii=False))

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


def translate_id_to_names_json():
    with open("data/-140.json", "r", encoding="utf-8") as file:
        timetable = file.read()
    timetable = json.loads(timetable)

    for i in range(len(timetable)):
        subjectid = timetable[i]['subjectid']
        classids = timetable[i]['classids']  # a list of classes that have this lesson
        timetable[i]['groupnames'] = timetable[i]['groupnames'][0]

        try:
            teacherids = timetable[i]['teacherids'][0]
        except:
            teacherids = ''
        try:
            colors = timetable[i]['colors'][0]  # color of the cell, e.g. #FFC000
            timetable[i]['colors'] = timetable[i]['colors'][0]
        except:
            timetable[i]['colors'] = "#FFFFE6"

        try:
            classroomids = timetable[i]['classroomids'][0]
            # id of a classroom
        except:
            classroomids = ''

        try:
            durationperiods = timetable[i]['durationperiods']
            # duration of the lesson, e.g. if the uniperiod = 3 and durationperiods = 2,
            # it means that the lesson will be from 3 to 4th lesson time
        except:
            timetable[i]['durationperiods'] = 1

        try:
            cellSlices = timetable[i]['cellSlices']  # These two are related, if cellSlices = "01", then cellorder = 1;
            cellOrder = timetable[i]['cellOrder']  # if cellSlices = "10", then cellorder = 0
        except Exception as ex:
            timetable[i]['cellSlices'] = '1'
            timetable[i]['cellOrder'] = 0
        # print(
        #     f"date={date}, uniperiod={uniperiod}, starttime={starttime}, endtime={endtime}, subjectid={subjectid}, classids={classids}, groupnames={groupnames}, teacherids={teacherids}, classroomids={classroomids}, colors={colors}, durationperiods={durationperiods}, cellSlices={cellSlices}, cellOrder={cellOrder}")

        # teacherids
        if (teacherids != ""):
            item = teachersdb.get_item(param="id", value=teacherids)
            if (item == None):
                item = ""
            else:
                item = item[1]
            print(item)
            timetable[i]['teacherids'] = item

            # classroomids
        if (classroomids != ""):
            item = classroomsdb.get_item(param="id", value=classroomids)
            if (item == None):
                item = ""
            else:
                item = item[1]

            timetable[i]['classroomids'] = item

            # classids
        if (classids != []):
            for j in range(len(classids)):
                item = classesdb.get_item(param="id", value=(classids[j]))
                if (item == None):
                    item = ""
                else:
                    item = item[1]
                timetable[i]['classids'][j] = item

            # subjectid
        if (subjectid != ""):
            item = subjectsdb.get_item(param="id", value=subjectid)
            if (item == None):
                item = ""
            else:
                item = item[1]
            # print(item)
            timetable[i]['subjectid'] = item
    with open(f"data/{classid}.json", "w", encoding='utf-8') as file:
        file.write(json.dumps(timetable, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    request_tt()
    translate_id_to_names_json()
    with open("data/-140.json", "r", encoding="utf-8") as file:
        timetable = file.read()
    timetable = json.loads(timetable)
    # timetable = json.dumps(timetable['r']['ttitems'], indent=4, ensure_ascii=False)
    # print(json.dumps(timetable, indent=4, ensure_ascii=False))
    # print(len(timetable['r']['ttitems']))

    fixed_timetable = []

    # previous_date = timetable['r']['ttitems'][0]['date']
    previous_date = timetable[0]['date']

    # timetable = timetable['r']['ttitems']
    for i in range(len(timetable)):
        date = timetable[i]['date']  # cell's current day
        uniperiod = timetable[i]['uniperiod']  # lesson number, e.g. 5 means that this cell starts from the 5 lesson
        starttime = timetable[i]['starttime']  # e.g. 08:15 for the 1st lesson
        endtime = timetable[i]['endtime']  # e.g. 09:50 for the 1st lesson
        subjectid = timetable[i]['subjectid']
        classids = timetable[i]['classids']  # a list of classes that have this lesson
        try:
            groupnames = timetable[i]['groupnames'][0]  # e.g. 2 группа
            timetable[i]['groupnames'] = timetable[i]['groupnames'][0]
        except:
            groupnames = ''
        try:
            teacherids = timetable[i]['teacherids'][0]
        except:
            teacherids = ''
        try:
            colors = timetable[i]['colors'][0]  # color of the cell, e.g. #FFC000
            timetable[i]['colors'] = timetable[i]['colors'][0]
        except:
            colors = "#FFFFE6"
            timetable[i]['colors'] = "#FFFFE6"

        try:
            classroomids = timetable[i]['classroomids'][0]
            # id of a classroom
        except:
            classroomids = ''

        try:
            durationperiods = timetable[i]['durationperiods']
            # duration of the lesson, e.g. if the uniperiod = 3 and durationperiods = 2,
            # it means that the lesson will be from 3 to 4th lesson time
        except:
            durationperiods = 1
        try:
            cellSlices = timetable[i]['cellSlices']  # For now, forget it
            cellOrder = timetable[i]['cellOrder']  # For now, forget it
        except Exception as ex:
            cellSlices = ''
            cellOrder = ''
        # print(
        #     f"date={date}, uniperiod={uniperiod}, starttime={starttime}, endtime={endtime}, subjectid={subjectid}, classids={classids}, groupnames={groupnames}, teacherids={teacherids}, classroomids={classroomids}, colors={colors}, durationperiods={durationperiods}, cellSlices={cellSlices}, cellOrder={cellOrder}")

        # teacherids
        if (teacherids != ""):
            item = teachersdb.get_item(param="id", value=teacherids)
            if (item == None):
                item = ""
            else:
                item = item[1]
            print(item)
            timetable[i]['teacherids'] = item

            # classroomids
        if (classroomids != ""):
            item = classroomsdb.get_item(param="id", value=classroomids)
            if (item == None):
                item = ""
            else:
                item = item[1]
            # print(item)
            timetable[i]['classroomids'] = item

            # classids
        if (classids != []):
            for j in range(len(classids)):
                item = classesdb.get_item(param="id", value=(classids[j]))
                if (item == None):
                    item = ""
                else:
                    item = item[1]
                timetable[i]['classids'][j] = item
            # print(item)
            # timetable[i]['classids'] = item

            # subjectid
        if (subjectid != ""):
            item = subjectsdb.get_item(param="id", value=subjectid)
            if (item == None):
                item = ""
            else:
                item = item[1]
            print(item)
            timetable[i]['subjectid'] = item
        # date, uniperiod, starttime, endtime, subjectid, classids, groupnames,
        # teacherid, colors, classroomids, durationperiods, cellSlices, cellOrder

        daycount = 0  # fixed timetable's iterator (j = 0 means monday, j = 1 means tuesday and etc.

        # fixed_timetable
        # if previous_date != date:
        #     fixed_timetable[j]
        #     pass
        # else:
        #     fixed_timetable.append({
        #
        #     })
        #     daycount+=1
    # with open(f"data/{classid}.json", "w", encoding='utf-8') as file:
    #     file.write(json.dumps(timetable, indent=4, ensure_ascii=False))

    print(json.dumps(timetable, indent=4, ensure_ascii=False))
    with open(f"data/{classesdb.get_item('id', classid)[1]}.json", "w") as file:
        file.write(json.dumps(fixed_timetable))
