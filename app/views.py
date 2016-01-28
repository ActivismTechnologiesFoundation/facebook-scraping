from flask import Blueprint, jsonify, make_response
from fb import get_events_for_group
from csv import convert_to_csv

api = Blueprint("api", __name__)

@api.route("/<groupId>/raw")
def get_events_raw(groupId):
    events = get_events_for_group(groupId)
    return jsonify(events=events)

@api.route("/<groupId>/csv")
def get_events_csv(groupId):
    events = get_events_for_group(groupId)
    csv_str = convert_to_csv(events)
    return csv_str
