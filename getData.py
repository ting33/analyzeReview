import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
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
#通过分析发现三个产品评论的时间不一致，为了方便下面的比较，只保留2019-6到2020-6月的数据
df=df[(df['data_ym']>=datetime.datetime(2019,6,1))&(df['data_ym']<=datetime.datetime(2020,6,1))]
# print(df.info())
# print(datetime.datetime.now().day)
# test=df['content'].value_counts()
#每个月商品的评论数量，画折线图
df_content=df.groupby(['short_name','data_ym'])['content'].count().reset_index().sort_values(by='data_ym')
p=df_content[df_content['short_name']=='Philips'].set_index('data_ym')
f=df_content[df_content['short_name']=='Fairywill'].set_index('data_ym')
o=df_content[df_content['short_name']=='Oral-B'].set_index('data_ym')
#画折线图
x=o.index
# print(p['content'])
# print(np.array(o['content']))
yp=np.array(p['content'])
yf=np.array(f['content'])
yo=np.array(o['content'])
plt.plot(x,yp,label='Philips')
plt.plot(x,yf,label='Fairywill')
plt.plot(x,yo,label='Oral-B')
plt.xlabel=('月份')
plt.ylabel=('注册量')
plt.xticks(x)
# plt.xticks(np.arange(1,14,1),['19年6月','19年7月','19年8月','19年9月','19年10月','19年11月','19年12月','20年1月','20年2月','20年3月','20年4月','20年5月','20年6月'])
plt.title("三个品牌每月的评论总数",loc='center')
plt.legend()
plt.show()
#每个月不同商品的好评率、差评率，质量监控
df_content1=df.groupby(['short_name','data_ym','stars_cat'])['content'].count().reset_index().sort_values(by='data_ym')
p_positive=df_content1[(df_content1['stars_cat']=='positive')&(df_content1['short_name']=='Philips')].set_index('data_ym')
p_negative=df_content1[(df_content1['stars_cat']=='negative')&(df_content1['short_name']=='Philips')].set_index('data_ym')
p_positive_ratio=round(p_positive['content']/p['content']*100,2).reset_index()
p_negative_ratio=round(p_negative['content']/p['content']*100,2).reset_index()
f_positive=df_content1[(df_content1['stars_cat']=='positive')&(df_content1['short_name']=='Fairywill')].set_index('data_ym')
f_negative=df_content1[(df_content1['stars_cat']=='negative')&(df_content1['short_name']=='Fairywill')].set_index('data_ym')
f_positive_ratio=round(f_positive['content']/f['content']*100,2).reset_index()
f_negative_ratio=round(f_negative['content']/f['content']*100,2).reset_index()
# print(f_positive['content'])
# print(f_negative['content'])
# print(f['content'])
# print(f_negative_ratio)
o_positive=df_content1[(df_content1['stars_cat']=='positive')&(df_content1['short_name']=='Oral-B')].set_index('data_ym')
o_negative=df_content1[(df_content1['stars_cat']=='negative')&(df_content1['short_name']=='Oral-B')].set_index('data_ym')
o_positive_ratio=round(o_positive['content']/o['content']*100,2).reset_index()
o_negative_ratio=round(o_negative['content']/o['content']*100,2).reset_index()
# yp_positive=np.array(p_positive_ratio['content'])
# yf_positive=np.array(f_positive_ratio['content'])
# yo_positive=np.array(o_positive_ratio['content'])
yp_negative=np.array(p_negative_ratio['content'])
yf_negative=np.array(f_negative_ratio['content'])
yo_negative=np.array(o_negative_ratio['content'])
# plt.plot(x,yp_positive,label='Philips')
# plt.plot(x,yf_positive,label='Fairywill')
# plt.plot(x,yo_positive,label='Oral-B')
plt.plot(x,yp_negative,label='Philips')
plt.plot(x,yf_negative,label='Fairywill')
plt.plot(x,yo_negative,label='Oral-B')
plt.xlabel=('月份')
plt.ylabel=('差评率%')
plt.xticks(x)
plt.legend()
plt.title("差评率",loc='center')
plt.show()
print(p_positive_ratio)
print(len(p_positive))
print(len(p))
print(p_positive_ratio)
print(o)
print(p.sort_values(by='data_ym'))



