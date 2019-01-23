import requests
import json


# res1 = requests.get("http://www.google.com")
# print(res1)
# print(res1.content)

"""
res2 = requests.get("https://swapi.co/api/people/1")
print(res2)
print(res2.content)
json_res2 = res2.json()
print(json_res2["name"], json_res2["height"], json_res2["mass"])
print(json.dumps(res2.json(), indent=1))
"""

# post = requests.post("https://en3r3ysp0i4cm.x.pipedream.net", data={"name" : "Upal"})
# post = requests.post("http://mockbin.org/bin/847d10c0-c503-45fa-b29b-00da68466cf0/view", data={"name" : "Upal"})
# print(post.content)

tweets = requests.get("https://twitter.com/search?q=%23@AfzalUpal%27")
print(tweets.headers)
print(tweets.text)
