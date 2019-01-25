from linkedin import linkedin

CLIENT_ID = ""
CLIENT_SECRET = ""
RETURN_URL = "http://localhost:8080"

auth = linkedin.LinkedInAuthentication(CLIENT_ID, CLIENT_SECRET, RETURN_URL)

print(auth.authorization_url)

"""
auth.authorization_code = ""

result = auth.get_access_token()
print(result.access_token)

app = linkedin.LinkedInApplication(token=result.access_token)

me = app.get_profile()

print(me)
"""
