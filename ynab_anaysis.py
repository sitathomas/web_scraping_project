import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
plt.style.use('ggplot')
pd.set_option('display.max_columns', None)

ynab = pd.read_csv("ynab/ynab.csv")

ynab["following"].fillna(0, inplace=True)

print(ynab.sample(1))