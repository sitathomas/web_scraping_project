import pandas as pd
import numpy as np
import nltk
import re
from matplotlib import pyplot as plt


plt.style.use('ggplot')
pd.set_option('display.max_columns', None)

ynab = pd.read_csv("ynab/ynab.csv")

by_date = ynab.sort_values('posted', ascending=False)
print("Newest post date:", by_date.posted.iloc[0])
print("Oldest post date:", by_date.posted.iloc[-1])

def top_stats(field):
  sort_ = ynab.sort_values(field, ascending=False)
  print("Most {}:".format(field), sort_[field].iloc[0])
top_stats("likes")
top_stats("replies")
top_stats("views")
top_stats("following")

ynab.text = ynab.text.str.lower()