import datetime
from dateutil import parser

from flask import current_app

KNOWN_COLUMNS = ["name", "link", "street_address", "city", "state",\
"start_date", "end_date", "description"]

def convert_to_csv(events):
    column_order = current_app.config["CSV_COLUMN_ORDER"]
    for c in column_order:
        if c not in KNOWN_COLUMNS:
            raise Exception("'%s' is not a valid column for csv")

    return "%s\n%s" % (",".join(column_order),\
            "\n".join([",".join(["\"" + event[c].replace('"', '""') + "\""\
            for c in column_order])\
            for event in parse_events(events)]))

def parse_events(events):
    return [parse_event(event) for event in events]

def parse_event(event):
    return {
        "name": _parse_name(event),
        "link": _parse_link(event),
        "street_address": _parse_street_address(event),
        "city": _parse_city(event),
        "state": _parse_state(event),
        "start_date": _parse_start_date(event),
        "end_date": _parse_end_date(event),
        "description": _parse_description(event)
    }

def _parse_name(event):
    return event.get("name", "")

def _parse_link(event):
    if "id" in event:
        return "https://www.facebook.com/events/%s" % event["id"]
    return ""

def _parse_street_address(event):
    if "place" in event:
        if "location" in event["place"]:
            if "street" in event["place"]["location"]:
                return event["place"]["location"]["street"]
            if "name" in event["place"]["location"]:
                return event["place"]["location"]["name"]
        return event["place"].get("name", "")
    return ""

def _parse_city(event):
    if "place" in event:
        if "location" in event["place"]:
            if "city" in event["place"]["location"]:
                return event["place"]["location"]["city"]
    return ""

def _parse_state(event):
    if "place" in event:
        if "location" in event["place"]:
            if "city" in event["place"]["location"]:
                return event["place"]["location"]["city"]
    return ""

def _parse_start_date(event):
    output_format = current_app.config["OUTPUT_TIMESTAMP_FORMAT"]
    if "start_time" in event:
        dt = parser.parse(event["start_time"])
        return datetime.datetime.strftime(dt, output_format)
    return ""

def _parse_end_date(event):
    output_format = current_app.config["OUTPUT_TIMESTAMP_FORMAT"]
    if "end_time" in event:
        dt = parser.parse(event["end_time"])
        return datetime.datetime.strftime(dt, output_format)
    return ""

def _parse_description(event):
    return event.get("description", "")
