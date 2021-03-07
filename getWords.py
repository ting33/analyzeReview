import nltk
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud

from changeData import getShortName, getColor, stars_cat, get_date, prepare_text_for_lda
from getPic import create_word_cloud
df = pd.read_excel('/Users/zhouya/Desktop/reviews.xlsx')
df = df.drop_duplicates(keep='first')
# 丢弃不需要列
df = df.drop(['buyer', 'short_content', 'reviews_url', 'asin', 'helpful', 'buyer_type'], axis=1)
df = df.dropna()
# print(df.info())
# 获得短名称
df['short_name'] = df['product_name'].apply(getShortName)
# 获取颜色
df['color'] = df['style'].apply(getColor)
# print(df['color'].value_counts())
# 把根据评分把评论分成好评、差评、中评三种
df['stars'] = df['stars'].apply(lambda s: float(s.replace(" out of 5 stars", '')))
df['stars_cat'] = df['stars'].apply(stars_cat)
#分析词云
positive_word=df[(df['short_name']=='Philips')&(df['stars_cat']=='positive')]['content']
# clean_positive=[prepare_text_for_lda(s) for s in positive_word]
# # wcloud = WordCloud().generate(''.join(str(i) for i in clean_positive))
# # plt.imshow(wcloud)
# # plt.axis('off')
# # plt.show()
# create_word_cloud(''.join(str(i) for i in clean_positive))

negative_word=df[(df['short_name']=='Philips')&(df['stars_cat']=='negative')]['content'].drop_duplicates(keep='first')
# negative_word=df[(df['short_name']=='Philips')&(df['stars_cat']=='negative')&(df['color']=='White')]['content']
clean_positive=[prepare_text_for_lda(s) for s in negative_word]
# print(clean_positive)
# s=" ".join(str(i) for i in clean_positive)
# print(type(s))
create_word_cloud(' '.join(str(i) for i in clean_positive))
# for i in negative_word:
#     if 'vibrate' in i:
#         print(i)
