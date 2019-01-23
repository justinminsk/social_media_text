from instagram.client import InstagramAPI


CLIENT_ID = "d38d4363531d4dbf9088b10e62603127"
client_secret = "693259dde6374541a4dffbc74e9066e6"

api = InstagramAPI(CLIENT_ID, client_secret)

user_id="jerrinjoe"

api.user(user_id)
print(api.user_media_feed())


