import pandas as pd
import numpy as np
import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import WordNetLemmatizer

from wordcloud import WordCloud
from matplotlib import pyplot as plt

from textblob import TextBlob

plt.style.use('ggplot')
pd.set_option('display.max_columns', None)

ynab = pd.read_csv("ynab/ynab.csv")
ynab.posted = pd.to_datetime(ynab.posted)
print()



print(ynab.posted.loc[ynab.posted>"2020-03-01 00:00:00",:])





#           ### USER STATS ###

# print("Number of posts:", len(ynab))
# print("Number of unique users:", len(set(ynab.user)))
# print("Average posts per user:", round(len(ynab) / len(set(ynab.user)), 2))
# posts_by_user = pd.DataFrame(ynab.groupby("user").size()).sort_values(0, ascending=False)
# posts_by_user["user"] = posts_by_user.index
# posts_by_user.index = range(0, len(posts_by_user))
# posts_by_user.columns = ["posts", "user"]
# posts_by_user["ratio"] = round(posts_by_user["posts"] / len(ynab), 3)
# posts_by_user = posts_by_user[["user", "posts", "ratio"]]
# print("Top 10 Users:\n", posts_by_user[:10])
# # print()

# #           ### DATE STATS ###
# # #~#~#~#~#~#~#~#~#~ HOW ELSE CAN THESE BE EXPANDED? #~#~#~#~#~#~#~#~#~

# by_date = ynab.sort_values('posted', ascending=False)
# print("Newest post date:", by_date.posted.iloc[0])
# print("Oldest post date:", by_date.posted.iloc[-1])
# print()



#           ### CATEGORY STATS ###

# def build_cat_stats(field):
#   return ynab.groupby("category")[field].sum()
# category_stats = pd.concat([ynab.groupby("category").category.count(), build_cat_stats("likes"), build_cat_stats("replies"), build_cat_stats("views"), build_cat_stats("following")], axis=1)
# category_stats.columns.values[0] = "posts"
# def build_cat_ratios(field):
#   category_stats["{}_ratio".format(field)] = 0
#   new_cells = []
#   for cell in category_stats[field]:
#     new_cells.append(round(cell / category_stats[field].sum(), 2))
#   category_stats["{}_ratio".format(field[0][0])] = new_cells
# category_stats = pd.concat([category_stats, build_cat_ratios("posts"), build_cat_ratios("likes"), build_cat_ratios("replies"), build_cat_ratios("views"), build_cat_ratios("following")])
# category_stats = category_stats[["posts", "p_ratio", "likes", "l_ratio", "replies", "r_ratio", "views", "v_ratio", "following", "f_ratio"]]
# print(category_stats.index)
# print()


#           ### AVERAGE STATS ###

# def avg_stats(field):
#   print("Average {}:".format(field), round(ynab.sort_values(field, ascending=False)[field].mean(), 2))
# avg_stats("likes")
# avg_stats("replies")
# avg_stats("views")
# avg_stats("following")
# print()



#           ### TOP STATS ###

# def top_stats(field):
#   top_post = ynab.sort_values(field, ascending=False)
#   print("Most {}:".format(field), top_post[field].iloc[0], "\n", top_post.iloc[0], "\n")
# top_stats("likes")
# top_stats("replies")
# top_stats("views")
# top_stats("following")
# print()



#           ### NLP PRE-PROCESSING ###

# stop_words = stopwords.words('english')
# # stop_words = stop_words + ["budget", "ynab", "account", "accounts", "transaction", "transactions", "money", "month", "category", "categories", "thank", "thanks", "make", "one", "way", "need", "want", "anyone", "know", "help", "question", "really", "hi", "thing", "https", "www", "etc"]

# # Clean text
# ynab.text = ynab.text.str.lower()
# ynab.text = ynab.text.apply(lambda x: re.sub('[^\w\s]', ' ', x))
# ynab.text = ynab.text.apply(lambda x: " ".join(word for word in x.split() if word not in stop_words))

# # Lemmatize
# ynab.text = ynab.text.apply(lambda x: ' '.join([WordNetLemmatizer().lemmatize(word) for word in x.split()]))

# # Tokenize
# tokens = ynab.text.apply(lambda x: word_tokenize(x))
# ynab.text = tokens.apply(lambda x: " ".join(sorted(set(x), key=x.index)))



#           ### WORD CLOUD FOR ALL CATEGORIES ###     NOT PARTICULARLY USEFUL

# wc = WordCloud(background_color="white", max_words=100, width=800, height=400)
# wc.generate(' '.join(ynab.text))
# plt.figure(figsize=(12, 6))
# plt.imshow(wc, interpolation='bilinear')
# plt.axis("off")
# plt.show()



#           ### BIGRAMS###

# def find_ngrams(words, n):
#     return list(zip(*[words[i:] for i in range(n)]))
# ynab["text_bigrams"] = ynab.text.apply(lambda x: find_ngrams(x.split(), 2))
# ynab.text_bigrams = ynab.text_bigrams.apply(lambda x: ['_'.join(tuples) for tuples in x])
# ynab.text_bigrams = ynab.text_bigrams.apply(lambda x: ' '.join(x))

# stop_bigrams = ["would_like", "even_though", "feel_like", "look_like", "go_back", "something_like", "let_say", "can_not", "make_sense", "trying_figure", "trying_get", "thing_like", "seems_like", "e_g", "every_time", "using_year", "get_rid", "thought_would"]

# ynab.text_bigrams = ynab.text_bigrams.apply(lambda x: " ".join(word for word in x.split() if word not in stop_bigrams))



#           ### WORD CLOUD FOR BIGRAMS ###

# wc = WordCloud(background_color="white", max_words=30, width=800, height=400)
# wc.generate(' '.join(ynab.text_bigrams))
# plt.figure(figsize=(12, 6))
# plt.imshow(wc, interpolation='bilinear')
# plt.axis("off")
# plt.show()



#           ### WORD CLOUDS FOR EACH CATEGORY ###

# cat_group = ynab.groupby("category")
# for category in cat_group:
#   wc = WordCloud(background_color="white", max_words=100, width=800, height=400)
#   wc.generate(' '.join(category[1].text))

#   plt.figure(num="{}".format(category[1].category), figsize=(12, 6))
#   plt.imshow(wc, interpolation='bilinear')
#   plt.axis("off")
#   plt.show()



#           ###SENTIMENT ANALYSIS ###

# def sentiment_func(x):
#     sentiment = TextBlob(x.text)
#     x['polarity'] = sentiment.polarity
#     x['subjectivity'] = sentiment.subjectivity
#     return x

# sample = ynab.apply(sentiment_func, axis=1)

# plt.scatter(sample.views, sample.polarity)
# plt.show()