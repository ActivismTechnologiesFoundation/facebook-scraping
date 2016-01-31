from flask import Blueprint, jsonify, make_response, request, g, current_app
from fb import get_events_for_group
from csv import convert_to_csv
from functools import wraps
from dateutil import parser

import datetime

api = Blueprint("api", __name__)

def get_epoch(dt):
    timestamp_format = current_app.config["ARG_TIMESTAMP_FORMAT"]
    dt = datetime.datetime.strptime(dt.strftime(timestamp_format),\
            timestamp_format)
    return int((dt - datetime.datetime.utcfromtimestamp(0)).total_seconds())

def get_common_params(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        default_max_results = current_app.config["FB_MAX_EVENT_RESULTS"]
        try:
            g.max_results = int(request.args.get("maxResults",\
                default_max_results))
        except ValueError:
            g.max_results = default_max_results

        default_since = datetime.datetime.now()
        try:
            if "from" in request.args:
                since_value = parser.parse(request.args.get("from"))
            else:
                since_value = default_since
            g.since = get_epoch(since_value)
        except ValueError:
            g.since = get_epoch(default_since)

        try:
            if "to" in request.args:
                until_value = parser.parse(request.args.get("to"))

                g.until = get_epoch(until_value)
            else:
                g.until = None
        except ValueError:
            g.until = None

        return func(*args, **kwargs)
    return wrapper

@api.route("/<groupId>/raw")
@get_common_params
def get_events_raw(groupId):
    events = get_events_for_group(groupId, g.max_results, g.since, g.until)
    return jsonify(events=events)

@api.route("/<groupId>/csv")
@get_common_params
def get_events_csv(groupId):
    events = get_events_for_group(groupId, g.max_results, g.since, g.until)
    csv_str = convert_to_csv(events)
    return csv_str

@api.route("/<groupId>/csv/download")
@get_common_params
def get_events_csv_download(groupId):
    events = get_events_for_group(groupId, g.max_results, g.since, g.until)
    csv_str = convert_to_csv(events)
    response = make_response(csv_str)
    response.headers["Content-Disposition"] = "attachment; filename=events.csv"
    return response

