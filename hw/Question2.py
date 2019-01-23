import tweepy
import time
import json

# add your keys here
con_key = ""
con_sec = ""
ac_token = ""
ac_sec = ""

# get your creds working with twitter api
auth = tweepy.OAuthHandler(con_key, con_sec)
auth.set_access_token(ac_token, ac_sec)

# set up the api for use
api = tweepy.API(auth)

# set up varibles to create lists
first_con_list = []
longest_follower_list = 0

# get user justinminsk informtaion and wait 15 mins if it gets a rate limit error
try:
    justinminsk = api.get_user("JustinMinsk")
except tweepy.RateLimitError:
    time.sleep(901)
    justinminsk = api.get_user("JustinMinsk")
# go through the followers that justinminsk has wait 15 mins if it hits a rate limit error 
try:
    for follower in justinminsk.followers():
        second_con_list = []
        # get info of a follower of justinminsk or wait 15 mins if it gets a rate limit error
        try:
            first_con = api.get_user(follower.screen_name)
        except tweepy.RateLimitError:
            time.sleep(901)
            first_con = api.get_user(follower.screen_name)
        # go through one of justinminsk followers followers and get there information
        try:
            for second_follower in first_con.followers():
                second_con_list.append(second_follower.screen_name)
        except tweepy.RateLimitError:
            time.sleep(901)
            for second_follower in first_con.followers():
                second_con_list.append(second_follower.screen_name)
        first_con_list.append({follower.screen_name : second_con_list})
        if len(second_con_list) > longest_follower_list:
            follower_with_most_followers = first_con.screen_name
except tweepy.RateLimitError:
        time.sleep(901)
        for follower in justinminsk.followers():
            second_con_list = []
            try:
                first_con = api.get_user(follower.screen_name)
            except tweepy.RateLimitError:
                time.sleep(901)
                first_con = api.get_user(follower.screen_name)
            try:
                for second_follower in first_con.followers():
                    second_con_list.append(second_follower.screen_name)
            except tweepy.RateLimitError:
                    time.sleep(901)
                    for second_follower in first_con.followers():
                        second_con_list.append(second_follower.screen_name)
            first_con_list.append({follower.screen_name : second_con_list})
            if len(second_con_list) > longest_follower_list:
                follower_with_most_followers = first_con.screen_name

# create a json style python dict with justinminsk info and the first con and second con list
final_json = {"user" : justinminsk.screen_name, "followers" : first_con_list}
# write to a json file
json.dump(final_json, open("question2.json", "w+"))
print(follower_with_most_followers)

f = open("question2.txt", "w+")
f.write("JustinMinsk Follower with Most Followers\n" + follower_with_most_followers)
    