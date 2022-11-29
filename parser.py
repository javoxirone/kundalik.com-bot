import requests
import json
from bs4 import BeautifulSoup
import re
from pprint import pprint
import datetime

url = 'https://login.kundalik.com/login'


def login(login, password):
    session = requests.Session()
    payload = {
        'login': login,
        'password': password
    }
    try:
        res = session.post('https://login.kundalik.com/login', json=payload)
        r = session.get('https://schools.kundalik.com/schedules').text
        # print(r)
        lessons_json = BeautifulSoup(r, 'html.parser')
        script = lessons_json.findAll('script')[-7].string
        data = \
            script.split("window.__USER__START__PAGE__INITIAL__STATE__ = ", 1)[1].split(
                'window.__TALK__INITIAL__STATE__')[
                0].rsplit(';', 1)[0]
        data = json.loads(data)

        marks = data['userMarks']['children'][0]['marks']
        todaySchedule = data['userSchedule']['children'][0]['schedule']['days'][0]['lessons']
        tomorrowSchedule = data['userSchedule']['children'][0]['schedule']['days'][1]['lessons']

        pprint(marks)
        pprint(todaySchedule)

        context = {'user_type': 'student', 'marks': marks, 'today_schedule': todaySchedule,
                   'tomorrow_schedule': tomorrowSchedule}
        return context
    except Exception as e:
        print(e)
        context = {'user_type': 'unknown', 'marks': "Something went wrong", 'today_schedule': "Something went wrong",
                   'tomorrow_schedule': "Something went wrong"}
        return context

# pprint(login('username', 'password'))
