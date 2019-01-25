from instagram.client import InstagramAPI


CLIENT_ID = ""
client_secret = ""

api = InstagramAPI(CLIENT_ID, client_secret)

user_id="jerrinjoe"

api.user(user_id)
print(api.user_media_feed())


