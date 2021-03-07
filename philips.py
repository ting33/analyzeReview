import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
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
# 处理日期
df['data_d'] = df['reviews_date'].apply(get_date)
# 日期具体到月，因为分析的时候具体到月，有问题了再下钻到日
df['data_ym'] = df['data_d'].dt.year.astype(str) + '-' + df['data_d'].dt.month.astype(str)
df['data_ym'] = pd.to_datetime(df['data_ym'])
df_content=df.groupby(['short_name','data_ym'])['content'].count().reset_index().sort_values(by='data_ym')
p=df_content[df_content['short_name']=='Philips'].set_index('data_ym')
q=p.reset_index()#为了方便筛选日期
print(q.head())
print(p.head())
x=np.array(p.index.strftime('%Y-%m-%d'))
# print(x[0:9])
# print(np.array(o['content']))
yp=np.array(p['content'])
plt.plot(x,yp,label='Philips')
plt.xlabel=('月份')
plt.ylabel=('注册量')
# plt.xticks(x)
plt.title("Philips每月的评论总数",loc='center')
plt.legend()
plt.show()
#分析每个月的数量变化
y8=np.array(q[q['data_ym']<=datetime.datetime(2018,12,1)]['content'])
print(y8)
y9=np.array(q[(q['data_ym']<=datetime.datetime(2019,12,1))&(q['data_ym']>datetime.datetime(2018,12,1))]['content'])
print(y9)
y2=np.array(q[q['data_ym']>datetime.datetime(2019,12,1)]['content'])
print(y2)
y18=[0,0,5,14,72,86,78,106,136,84,88,168]
y19=[162,100,174,190,244,270,351,290,219,269,306,682]
y20=[821,622,360,228,245,300,283,0,0,0,0,0]
x892=np.arange(12)
print(x892)
plt.bar(x892,y18,width=0.3,label='2018年')
plt.bar(x892+0.3,y19,width=0.3,label='2019年')
plt.bar(x892+0.6,y20,width=0.3,label='2020年')
plt.title("每个月评论数量",loc='center')
for a,b in zip(x892,y18):
    plt.text(a,b,b,ha='center',va='bottom',fontsize=12)
for a,b in zip(x892+0.3,y19):
    plt.text(a,b,b,ha='center',va='bottom',fontsize=12)
for a,b in zip(x892+0.6,y20):
    plt.text(a,b,b,ha='center',va='bottom',fontsize=12)
plt.xticks(x892+0.45,['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'])
plt.xlabel=('月份')
plt.ylabel=('评论数量')
plt.legend()
plt.show()

df_content1=df.groupby(['short_name','data_ym','stars_cat'])['content'].count().reset_index().sort_values(by='data_ym')
p_positive=df_content1[(df_content1['stars_cat']=='positive')&(df_content1['short_name']=='Philips')].set_index('data_ym')
p_negative=df_content1[(df_content1['stars_cat']=='negative')&(df_content1['short_name']=='Philips')].set_index('data_ym')
p_neutral=df_content1[(df_content1['stars_cat']=='neutral')&(df_content1['short_name']=='Philips')].set_index('data_ym')
print(p_positive['content'].sum())
print(p_negative['content'].sum())
print(p_neutral['content'].sum())
p_positive_ratio=round(p_positive['content']/p['content']*100,2).reset_index()

p_negative_ratio=round(p_negative['content']/p['content']*100,2).reset_index()
print(p_negative_ratio.mean())
yp_negative=np.array(p_negative_ratio['content'])
yp_positive=np.array(p_positive_ratio['content'])
# print(p_negative_ratio)

plt.plot(x,yp_positive)
plt.xlabel=('月份')
plt.ylabel=('好评率%')
plt.xticks(x)
plt.title("好评率",loc='center')
plt.show()


plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
labels = ['好评','差评','中评']
sizes = [p_positive['content'].sum(),p_negative['content'].sum(),p_neutral['content'].sum()]
explode = (0.1,0,0) #距离中心的距离
plt.pie(sizes,explode=explode,labels=labels,autopct='%1.1f%%',shadow=False,startangle=150)
plt.title("2019年6月-2020年6月好中差评占比")
plt.show()
#颜色分析
p_color=df[df['short_name']=='Philips']
c=p_color['color'].value_counts()
labels = c.index
sizes = [c['Black'],c['White'],c['Pink']]
explode = (0,0,0) #距离中心的距离
plt.pie(sizes,explode=explode,labels=labels,autopct='%1.1f%%',shadow=False,startangle=150)
plt.title("颜色评论占比")
plt.show()
#不同颜色好评率占比
p_dif_color=df.groupby(['color','stars_cat']).count().reset_index()
print(p_dif_color)
labels =['差评','中评','好评']
size1 = [1358,496,9315]
explode = (0,0,0) #距离中心的距离
plt.subplot(2,2,1)
plt.pie(size1,explode=explode,labels=labels,autopct='%1.1f%%',shadow=False,startangle=150)
plt.title("黑色评论占比")
size2 = [62,24,535 ]
explode = (0,0,0) #距离中心的距离
plt.subplot(2,2,2)
plt.pie(size2,explode=explode,labels=labels,autopct='%1.1f%%',shadow=False,startangle=150)
plt.title("粉色评论占比")
size3 = [827,236,3869]
explode = (0,0,0) #距离中心的距离
plt.subplot(2,2,3)
plt.pie(size3,explode=explode,labels=labels,autopct='%1.1f%%',shadow=False,startangle=150)
plt.title("白色评论占比")
plt.show()
