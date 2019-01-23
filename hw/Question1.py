import tweepy
import json
import time
import pandas as pd

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
tweet_list = []

print("Getting Tweets")
for tweet in tweepy.Cursor(api.search, q='python', rpp=100).items(1000):
    read_tweet = tweet._json
    tweet_list.append(read_tweet)

tweet_dict = {"tweets" : tweet_list}
print("Dumpping Tweets to a Json file")
json.dump(tweet_dict, open("question1.json", "w+"))

tweet_dataframe = pd.DataFrame(tweet_list)
print("Saving pickle of tweet dataframe")
tweet_dataframe.to_pickle("1000_tweets.pkl")

# if you want to use the same comment out to before the import statement
tweet_dataframe = pd.read_pickle("1000_tweets.pkl")

# write anwers to a text file
f = open("question1.txt", "w+")

# get highest retweeted tweet and print/write to text file
highest_retweets = tweet_dataframe.loc[tweet_dataframe.retweet_count == tweet_dataframe.retweet_count.max()]
f.write("Highest ReTweeted Tweet \n")
f.write(highest_retweets.to_string())
print("Highest ReTweeted Tweet")
print(highest_retweets)

# get highest favorited tweet and print/write to text file
highest_favorites = tweet_dataframe.loc[tweet_dataframe.favorite_count == tweet_dataframe.favorite_count.max()]
f.write("\nHighest Favored Tweet \n")
f.write(highest_favorites.to_string())
print("Highest Favored Tweet")
print(highest_favorites)

f.close()
