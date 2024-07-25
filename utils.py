import datetime
import os


def parseDate(date: str) -> datetime.datetime:
    return datetime.datetime.strptime(date, "%Y-%m-%d")


def parseDatetime(dt: str) -> datetime.datetime:
    return datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S%z")


def parseDateOrDatetime(data: object) -> datetime.datetime:
    if "date" in data:
        return parseDate(data["date"])
    else:
        return parseDatetime(data["dateTime"])


def clearTerminal():
    os.system("cls" if os.name == "nt" else "clear")
