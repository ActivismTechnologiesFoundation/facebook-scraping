from flask import current_app

import facebook

def get_events_for_group(group_id):
    access_token = facebook.get_app_access_token(\
            current_app.config["FB_APP_ID"],\
            current_app.config["FB_APP_SECRET"])

    graph_api = facebook.GraphAPI(access_token=access_token)

    return graph_api.get_object("%s/events" % group_id)["data"]
