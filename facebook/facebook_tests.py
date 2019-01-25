import facebook
import json


def pp(o):
    print(json.dumps(o, indent=1))

# has to be refrreshed 
token=" "

graph = facebook.GraphAPI(access_token=token, version="2.12")

pp(graph.get_connections(id="me", connection_name="feed"))
