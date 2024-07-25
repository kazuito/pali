import datetime
import time
import utils

from googleapiclient.discovery import build

import auth


def show_events():
    creds = auth.auth()

    service = build("calendar", "v3", credentials=creds)

    todayBegin = datetime.datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    tomorrowBegin = todayBegin + datetime.timedelta(days=1)

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=todayBegin.isoformat() + "Z",
            maxResults=30,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return

    todaysEvents = [
        e for e in events if utils.parseDateOrDatetime(e["start"]).date() == todayBegin.date()
    ]

    tomorrowsEvents = [
        e for e in events if utils.parseDateOrDatetime(e["start"]).date() == tomorrowBegin.date()
    ]

    upcomingEvents = [
        e
        for e in events
        if utils.parseDateOrDatetime(e["start"]) != todayBegin
        and utils.parseDateOrDatetime(e["start"]) != tomorrowBegin
    ]

    todayText = todayBegin.strftime("%a %m/%d")
    tomorrowText = tomorrowBegin.strftime("%a %m/%d")

    print(f"{todayText} Today")
    print("---------------")
    for e in todaysEvents:
        print(f" - {e['summary']}")

    print("")
    print(f"{tomorrowText} Tomorrow")
    print("---------------")
    for e in tomorrowsEvents:
        print(f" - {e['summary']}")

    print("")
    print("Upcoming Events")
    print("---------------")
    for e in upcomingEvents:
        dateText = utils.parseDateOrDatetime(e["start"]).strftime("%a %m/%d")
        print(f" - {dateText} {e['summary']}")


def main():
    interval = 60 * 10
    while True:
        utils.clearTerminal()
        show_events()
        time.sleep(interval)


if __name__ == "__main__":
    main()
