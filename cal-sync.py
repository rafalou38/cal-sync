from ics import Calendar
from datetime import timedelta
import arrow
import requests
import re

horaires = {
    8: [8, 0],
    9: [8, 55],
    10: [10, 10],
    11: [11, 5],
    12: [12, 0],
    13: [13, 0],
    14: [13, 55],
    15: [14, 55],
    16: [16, 0],
    17: [16, 55],
}


url = "https://0383243u.index-education.net/pronote/ical/Edt.ics?icalsecurise=EEFC26724EC5C4BCAF79E4D3FCFAD22CCAD6990EA20E1A8DDB4628D72D50C858866C2980D0F06CBA0A81005955FF2731&version=2022.0.3.1&param=66683d31"
c = Calendar(requests.get(url).text)

local = arrow.now("Europe/Paris").tzinfo
for i, e in enumerate(set(c.events)):
    # datetime_obj = datetime.fromisoformat()
    begin = e.begin.astimezone(local)
    if not e.duration:
        continue

    if re.search(r"annulé|absent", e.name, re.UNICODE):
        c.events.remove(e)

    try:
        newt = horaires[begin.hour]
    except:
        continue

    d_h = e.duration.seconds / (60 * 60)
    e.duration = timedelta(seconds=e.duration.seconds - (60 * 5 * d_h))

    e.begin = begin.replace(hour=newt[0], minute=newt[1])

    if e.location:
        e.name = e.location.split("x")[0] + e.name.split(" - ")[0]


with open("/var/www/static/edt.ics", "wb") as f:
    f.write(bytes(c.serialize().replace("\n\r", "\n"), encoding="utf-8"))
