import fastparquet
import re
import nltk
import datetime
import logging
import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.externals import joblib


logging.basicConfig(filename='model.txt', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

"""
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

df = pd.DataFrame({"user_id": tweets_df.id_str, "date_col": tweets_df.created_at, "tweets_col": tweets_df.text,
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
df = df.reset_index()

# See if I need to convert some columns
# print(df.dtypes)

df.date_col = pd.to_datetime(df.date_col)
df["hour"] = pd.to_numeric(df.date_col.dt.hour)
df["day"] = pd.to_numeric(df.date_col.dt.dayofyear)
df["time_since"] = pd.to_numeric((datetime.datetime.now() - df.date_col).dt.total_seconds())
# get hours since seconds is too large
df["time_since"] = df["time_since"]/3600
df["interaction"] = df.favorite_count + df.retweet_count
df = df.drop(["date_col", "favorite_count", "retweet_count", "user_id"], axis=1)

# Lower case text
df.tweets_col = df.tweets_col.str.lower()

# regex 
df.tweets_col = df.tweets_col.apply(pre_processing)

print(df.head())

# Had problems geting columns correct
print("Before adding grams:",df.shape)

# word grams with stop words
word_grams = TfidfVectorizer(analyzer = "word", ngram_range = (2, 4), stop_words="english")

word_vector = word_grams.fit_transform(df.tweets_col)

word_df = pd.DataFrame()

# https://stackoverflow.com/questions/43577590/adding-sparse-matrix-from-countvectorizer-into-dataframe-with-complimentary-info
for i, col in enumerate(word_grams.get_feature_names()):
    word_df[col] = pd.Series(word_vector[:, i].toarray().ravel())

# char grams with stop words
char_grams = TfidfVectorizer(analyzer = "char", ngram_range = (3, 4), stop_words="english")

char_vector = char_grams.fit_transform(df.tweets_col)

char_df = pd.DataFrame()

for i, col in enumerate(char_grams.get_feature_names()):
    char_df[col] = pd.Series(char_vector[:, i].toarray().ravel())

df2 = pd.merge(df, char_df, left_index=True, right_index=True)   
end_df = pd.merge(df2, word_df, left_index=True, right_index=True) 

print("After Char and Word Grams:", end_df.shape)

end_df = end_df.drop(["tweets_col"], axis=1)

# CSV's are gross for loading and saving
fastparquet.write("processed_tweets_2.parquet", end_df)
df.to_csv("processed_tweets.csv")
"""
df = pd.read_parquet("processed_tweets_2.parquet")

# might look into this more seems like some tweets are not being processed
# Fixed
df = df.dropna()

print("Scaling Data")

non_word_columns = ["time_since", "day", "hour"]

x_data = df.drop(["interaction"], axis=1)
print("Shape x_data:", x_data.shape)

y_data = df.interaction.values
print("Shape y_data:", y_data.shape)

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.10, random_state=42)

y_train_cat = pd.cut(y_train, bins=3, labels=False)
y_test_cat = pd.cut(y_test, bins=3, labels=False)


print("x Train:", x_train.shape)
print("y Trian", y_train.shape)


params = {"max_depth" : list(range(20, 30))}
grid_search_cv = GridSearchCV(DecisionTreeRegressor(random_state=1), params, n_jobs=1, verbose=1)
grid_search_cv.fit(x_train, y_train)
print("Decision Tree Grid Search:")
print(grid_search_cv.best_estimator_)
joblib.dump(grid_search_cv.best_estimator_, "saved_models/dtr.joblib")
"""
DecisionTreeRegressor(criterion='mse', max_depth=24, max_features=None,
           max_leaf_nodes=None, min_impurity_decrease=0.0,
           min_impurity_split=None, min_samples_leaf=1,
           min_samples_split=2, min_weight_fraction_leaf=0.0,
           presort=False, random_state=1, splitter='best')
"""
params = {"max_depth" : list(range(1, 20))}
grid_search_cv = GridSearchCV(RandomForestRegressor(random_state=1), params, n_jobs=1, verbose=1)
grid_search_cv.fit(x_train, y_train)
print("Random Forest Grid Search:")
print(grid_search_cv.best_estimator_)
joblib.dump(grid_search_cv.best_estimator_, "saved_models/rfr.joblib")
"""
RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=13,
           max_features='auto', max_leaf_nodes=None,
           min_impurity_decrease=0.0, min_impurity_split=None,
           min_samples_leaf=1, min_samples_split=2,
           min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,
           oob_score=False, random_state=1, verbose=0, warm_start=False)
"""
params = {"max_depth" : list(range(5, 50))}
grid_search_cv = GridSearchCV(DecisionTreeClassifier(random_state=1), params, n_jobs=1, verbose=1)
grid_search_cv.fit(x_train, y_train_cat)
print("Decision Tree Grid Search:")
print(grid_search_cv.best_estimator_)
joblib.dump(grid_search_cv.best_estimator_, "saved_models/dtc.joblib")
"""
DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=5,
            max_features=None, max_leaf_nodes=None,
            min_impurity_decrease=0.0, min_impurity_split=None,
            min_samples_leaf=1, min_samples_split=2,
            min_weight_fraction_leaf=0.0, presort=False, random_state=1,
            splitter='best')
"""
params = {"max_depth" : list(range(5,20))}
grid_search_cv = GridSearchCV(RandomForestClassifier(random_state=1), params, n_jobs=1, verbose=1)
grid_search_cv.fit(x_train, y_train_cat)
print("Random Forest Grid Search:")
print(grid_search_cv.best_estimator_)
joblib.dump(grid_search_cv.best_estimator_, "saved_models/rfc.joblib")
"""
RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=5, max_features='auto', max_leaf_nodes=None,
            min_impurity_decrease=0.0, min_impurity_split=None,
            min_samples_leaf=1, min_samples_split=2,
            min_weight_fraction_leaf=0.0, n_estimators=10, n_jobs=1,
            oob_score=False, random_state=1, verbose=0, warm_start=False)
"""

# Look at Scores
dtr = joblib.load("saved_models/dtr.joblib")
fi_dict = dict(zip(x_train.columns, dtr.feature_importances_))
logging.info({ k:v for k, v in fi_dict.items() if v })
print(dtr.score(x_test, y_test))
# Look at Scores
rfr = joblib.load("saved_models/rfr.joblib")
print(rfr.score(x_test, y_test))
# Look at Scores
dtc = joblib.load("saved_models/dtc.joblib")
fi_dict = dict(zip(x_train.columns, dtc.feature_importances_))
logging.info({ k:v for k, v in fi_dict.items() if v })
print(dtc.score(x_test, y_test_cat))
# Look at Scores
rfc = joblib.load("saved_models/rfc.joblib")
print(rfc.score(x_test, y_test_cat))

