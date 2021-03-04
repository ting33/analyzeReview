import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from changeData import getShortName, getColor, stars_cat, get_date
pd.set_option('Display.max_columns', None)
df=pd.read_excel('/Users/zhouya/Desktop/reviews.xlsx')
# print(df.head())
# print(df.isnull().sum())
df = df.drop_duplicates(keep='first')
#丢弃不需要列
df=df.drop(['buyer','short_content','reviews_url','asin','helpful','buyer_type'],axis=1)
df=df.dropna()
print(df.info())
#获得短名称
df['short_name']=df['product_name'].apply(getShortName)
#获取颜色
df['color']=df['style'].apply(getColor)
print(df['color'].value_counts())
#把根据评分把评论分成好评、差评、中评三种
df['stars']=df['stars'].apply(lambda s:float(s.replace(" out of 5 stars",'')))
df['stars_cat']=df['stars'].apply(stars_cat)
#处理日期
df['data_d']=df['reviews_date'].apply(get_date)
#日期具体到月，因为分析的时候具体到月，有问题了再下钻到日
df['data_ym']=df['data_d'].dt.year.astype(str)+'-'+df['data_d'].dt.month.astype(str)
df['data_ym']=pd.to_datetime(df['data_ym'])
print(df.info())
test=df['content'].value_counts()
#每个月商品的评论数量
df_content=df.groupby(['short_name','data_ym'])['content'].count().reset_index().sort_values(by='data_ym')
p=df_content[df_content['short_name']=='Philips'].set_index('data_ym')
f=df_content[df_content['short_name']=='Fairywill']
o=df_content[df_content['short_name']=='Oral-B']
#每个月不同商品的好评率、差评率，质量监控
df_content1=df.groupby(['short_name','data_ym','stars_cat'])['content'].count().reset_index().sort_values(by='data_ym')
p_positive=df_content1[(df_content1['stars_cat']=='positive')&(df_content1['short_name']=='Philips')].set_index('data_ym')
p_negative=df_content1[(df_content1['stars_cat']=='negative')&(df_content1['short_name']=='Philips')]
p_positive_ratio=round(p_positive['content']/p['content']*100,2)
print(type(p_positive_ratio))
print(len(p_positive))
print(len(p))
print(p_positive_ratio)
print(o)
print(p.sort_values(by='data_ym'))

