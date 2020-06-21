import pandas as pd
import numpy as np
import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import WordNetLemmatizer
from nltk.probability import FreqDist

from wordcloud import WordCloud
from matplotlib import pyplot as plt


plt.style.use('ggplot')
pd.set_option('display.max_columns', None)

ynab = pd.read_csv("ynab/ynab.csv")
print()
print("Columns:\n", ynab.columns.tolist())
print()
print("Number of posts:", len(ynab))
print("Number of unique users:", len(set(ynab.user)))
user_group = pd.DataFrame(ynab.groupby("user").size()).sort_values(0, ascending=False)
user_group["user"] = user_group.index
user_group.index = range(1, len(user_group)+1)
user_group.columns = ["posts", "user"]
user_group["percent"] = round(user_group["posts"] / 7142 * 100, 2)
user_group = user_group[["user", "posts", "percent"]]
print("Top 10 Users:\n", user_group[:10])
print()
by_date = ynab.sort_values('posted', ascending=False)
print("Newest post date:", by_date.posted.iloc[0])
print("Oldest post date:", by_date.posted.iloc[-1])
print()
def top_stats(field):
  top_post = ynab.sort_values(field, ascending=False)
  print("Most {}:".format(field), top_post[field].iloc[0], "\nTitle: {}".format(top_post.title.iloc[0]))
top_stats("likes")
top_stats("replies")
top_stats("views")
top_stats("following")
print()
def avg_stats(field):
  print("Average {}:".format(field), round(ynab.sort_values(field, ascending=False)[field].mean(), 2))
avg_stats("likes")
avg_stats("replies")
avg_stats("views")
avg_stats("following")






# def category_stats(field):
#   cat_group = ynab.groupby("category")
#   for key, values in cat_group:
#     print("Number of {} per {}:".format(field, key), sum(values[field]))
# category_stats("likes")
# category_stats("replies")
# category_stats("views")
# category_stats("following")
# # cat_group = ynab.groupby("category")
# # for key, values in cat_group:
# #   print(sum(values.likes))
# print("\nNumber of posts per category:\n", ynab.groupby("category").category.count())



### NLP PRE-PROCESSING ###
# ynab.text = ynab.text.str.lower()
# ynab.text = ynab.text.apply(lambda x: re.sub('[^\w\s]', ' ', x))
# ynab.text = ynab.text.apply(lambda x: " ".join(word for word in x.split() if word not in stop_words))

# stop_words = stopwords.words('english')
# stop_words = stop_words + ["budget", "ynab", "account", "accounts", "transaction", "transactions", "money", "month", "category", "categories", "thank", "thanks", "make", "one", "way", "need", "want", "anyone", "know", "help", "question", "really", "hi", "thing", "https", "etc"]

# tokens = ynab.text.apply(lambda x: word_tokenize(x))
# ynab.text = tokens.apply(lambda x: " ".join((set(x))))

# WNL = WordNetLemmatizer()
# ynab.text = ynab.text.apply(lambda x: ' '.join([WNL.lemmatize(word) for word in x.split()]))



### N GRAMS###
# def find_ngrams(input_list, n):
#     return list(zip(*[input_list[i:] for i in range(n)]))
# text_ngrams = ynab.text.apply(lambda x: find_ngrams(x.split(), 3))
# print(text_ngrams[0])

### WORD CLOUD FOR ALL CATEGORIES ###
# wc = WordCloud(background_color="white", max_words=100, width=800, height=400)
# wc.generate(' '.join(ynab.text))
# plt.figure(figsize=(12, 6))
# plt.imshow(wc, interpolation='bilinear')
# plt.axis("off")
# plt.show()

### WORD CLOUDS FOR EACH CATEGORY ###
# accts_trans = ynab.groupby("category")
# for item in accts_trans:
#   wc = WordCloud(background_color="white", max_words=100, width=800, height=400)
#   wc.generate(' '.join(item[1].text))

#   plt.figure(num="{}".format(item[1].category), figsize=(12, 6))
#   plt.imshow(wc, interpolation='bilinear')
#   plt.axis("off")
#   plt.show()
