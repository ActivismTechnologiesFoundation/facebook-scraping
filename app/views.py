from flask import Blueprint, jsonify
from fb import get_events_for_group

api = Blueprint("api", __name__)

@api.route("/<groupId>/raw")
def get_events_raw(groupId):
    events = get_events_for_group(groupId)
    return jsonify(events=events)
