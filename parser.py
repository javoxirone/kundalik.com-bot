import requests
import json
from bs4 import BeautifulSoup
import re
from pprint import pprint

url = 'https://login.kundalik.com/login'


def login(login, password):
    try:
        session = requests.Session()
        payload = {
            'login': login,
            'password': password
        }
        res = session.post('https://login.kundalik.com/login', json=payload)
        # s.headers.update({'authorization': json.loads(res.content)['token']})
        # print(res.content)
        r = session.get('https://schools.kundalik.com/schedules').text
        lessons_json = BeautifulSoup(r, 'html.parser')
        script = lessons_json.findAll('script')[-8].string

        data = \
            script.split("window.__USER__START__PAGE__INITIAL__STATE__ = ", 1)[1].split('window.__TALK__INITIAL__STATE__')[
                0].rsplit(';', 1)[0]
        data = json.loads(data)

        marks = data['userMarks']['children'][0]['marks']
        todaySchedule = data['userSchedule']['children'][0]['schedule']['days'][0]['lessons']
        tomorrowSchedule = data['userSchedule']['children'][0]['schedule']['days'][1]['lessons']

        pprint(marks)
        pprint(todaySchedule)

        # print(data)
        # data = re.search(r"\['__USER__START__PAGE__INITIAL__STATE__'\]\s*=\s*(.*);", r.text)
        # print(r.text)
        # print(requests.get('https://schools.kundalik.com/schedules/view.aspx?school=1000000248498&group=1984364230495136348').text)
        context = {'marks': marks, 'today_schedule': todaySchedule, 'tomorrow_schedule': tomorrowSchedule}
        return context
    except Exception as e:
        print(e)
        return {'marks': "To'gri malumot kiriting", 'schedule': "To'gri malumot kiriting", 'tomorrow_schedule': "To'gri malumot kiriting"}

# pprint(login('nurmatjonovjavoxir', 'Bilmayman06$'))