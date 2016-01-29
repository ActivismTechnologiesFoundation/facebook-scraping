from flask import Blueprint, jsonify, make_response, request, g, current_app
from fb import get_events_for_group
from csv import convert_to_csv
from functools import wraps

api = Blueprint("api", __name__)

def get_common_params(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        default_max_results = current_app.config["FB_MAX_EVENT_RESULTS"]
        g.max_results = int(request.args.get("maxResults",\
            default_max_results))
        return func(*args, **kwargs)
    return wrapper

@api.route("/<groupId>/raw")
@get_common_params
def get_events_raw(groupId):
    events = get_events_for_group(groupId, g.max_results)
    return jsonify(events=events)

@api.route("/<groupId>/csv")
@get_common_params
def get_events_csv(groupId):
    events = get_events_for_group(groupId, g.max_results)
    csv_str = convert_to_csv(events)
    return csv_str

@api.route("/<groupId>/csv/download")
@get_common_params
def get_events_csv_download(groupId):
    events = get_events_for_group(groupId, g.max_results)
    csv_str = convert_to_csv(events)
    response = make_response(csv_str)
    response.headers["Content-Disposition"] = "attachment; filename=events.csv"
    return response

