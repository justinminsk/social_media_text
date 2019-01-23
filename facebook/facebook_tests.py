import facebook
import json


def pp(o):
    print(json.dumps(o, indent=1))

# has to be refrreshed 
token="EAAK5QV4mkgcBADTKxGwaPzDlzTGM4e9JFkrl6P0cO9dOkb771fmmwg7NQkvVpwJy2mFvmx8rSvAgITSnaIIw20uHq6JICWejyyZChGJpPO1X15gBua9gMIlZBmFVREwz8KW33ViaSZAUw9Ftss1fpCZBZBFBpqSDx62738pbJXrHTbF2iKH31F9H4QTBbaVbmthGLNC0NZBQZDZD"

graph = facebook.GraphAPI(access_token=token, version="2.12")

pp(graph.get_connections(id="me", connection_name="feed"))
