from flask import current_app

import facebook
import requests

def get_events_for_group(group_id, max_results, since, until=None):
    access_token = facebook.get_app_access_token(\
            current_app.config["FB_APP_ID"],\
            current_app.config["FB_APP_SECRET"])

    modifiers = {"since": since}
    if until:
        modifiers["until"] = until

    graph_api = facebook.GraphAPI(access_token=access_token)
    raw_events = graph_api.get_object(("%s/events" % group_id), **modifiers)

    events = []
    cursor = 0
    while cursor < max_results:
        try:
            for event in raw_events["data"]:
                if cursor >= max_results:
                    break
                events.append(event)
                cursor += 1
            if cursor < max_results:
                raw_events = requests.get(raw_events["paging"]["next"]).json()
        except KeyError:
            break

    return events
