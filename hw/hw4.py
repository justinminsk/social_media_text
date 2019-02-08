import fastparquet
import re
import nltk
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer

# https://stackoverflow.com/questions/51417970/list-of-dictionaries-to-dataframe
def flatten(kv, prefix=[]):
    for k, v in kv.items():
        if isinstance(v, dict):
            yield from flatten(v, prefix+[str(k)])
        else:
            if prefix:
                yield '_'.join(prefix+[str(k)]), v
            else:
                yield str(k), v

pat1 = r'@[A-Za-z0-9_]+'
pat2 = r'https?://[^ ]+'
combined_pat = r'|'.join((pat1,pat2))
www_pat = r'www.[^ ]+'
negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                "mustn't":"must not"}
neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')

def pre_processing(row):
    first_process = re.sub(combined_pat, '', row)
    second_process = re.sub(www_pat, '', first_process)
    third_process = second_process.lower()
    fourth_process = neg_pattern.sub(lambda x: negations_dic[x.group()], third_process)
    result = re.sub(r'[^A-Za-z ]','',fourth_process)
    return result.strip()

############################
##### ADD JSON FILE HERE ###
############################
tweets = pd.read_json("question1.json")

tweets_df = pd.DataFrame({k:v for k, v in flatten(kv)} for kv in tweets.tweets)

# print(tweets_df.columns.tolist())

df = pd.DataFrame({"user_id": tweets_df.id_str, "date": tweets_df.created_at, "text": tweets_df.text,
                     "favorite_count": tweets_df.favorite_count, "retweet_count": tweets_df.retweet_count,
                     "lang": tweets_df.lang})

df.favorite_count = df.favorite_count.fillna(0)
df.retweet_count = df.retweet_count.fillna(0)

print(df.head())

# Faster than reading in the json file
# fastparquet.write("1000_tweets.parquet", df)
# df = pd.read_parquet("1000_tweets.parquet")

print("Before removing non-English tweets:",df.shape[0])

# Have a few non-english tweets
df = df[df.lang == "en"]

print("After removing non-English tweets:",df.shape[0])

df = df.drop(["lang"], axis=1)

# See if I need to convert some columns
# print(df.dtypes)

df.date = pd.to_datetime(df.date)

# Lower case text
df.text = df.text.str.lower()

# regex 
df.text = df.text.apply(pre_processing)

# Had problems geting columns correct
print("Before adding grams:",df.shape)

# word grams with stop words
word_grams = CountVectorizer(analyzer = "word", ngram_range = (2, 4), stop_words="english")

word_vector = word_grams.fit_transform(df.text)

# https://stackoverflow.com/questions/43577590/adding-sparse-matrix-from-countvectorizer-into-dataframe-with-complimentary-info
for i, col in enumerate(word_grams.get_feature_names()):
    df[col] = pd.Series(word_vector[:, i].toarray().ravel())

print("After word grams:",df.shape)

# char grams with stop words
char_grams = CountVectorizer(analyzer = "char", ngram_range = (3, 4), stop_words="english")

char_vector = char_grams.fit_transform(df.text)

for i, col in enumerate(char_grams.get_feature_names()):
    df[col] = pd.Series(char_vector[:, i].toarray().ravel())

print("After char grams:",df.shape)

# CSV's are gross for loading and saving
fastparquet.write("processed_tweets.parquet", df)
df.to_csv("processed_tweets.csv")
