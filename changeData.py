import pandas as pd
from nltk.corpus import wordnet as wn
import nltk
#把productname处理一下，使用缩略名代替，经过观察一共只有三个品牌
def getShortName(s):
    if 'Philips' in s:
        return 'Philips'
    elif 'Fairywill' in s:
        return 'Fairywill'
    else:
        return 'Oral-B'

# 从style提取出颜色
def getColor(s):
    if 'Black' in s:
        return 'Black'
    elif 'White' in s:
        return 'White'
    elif 'Pink' in s:
        return 'Pink'
    else:
        return 'Green'

def stars_cat(n):
    if n<=2:
        return 'negative'
    elif n==3:
        return 'neutral'
    return 'positive'

#处理日期
def get_date(x):
    x=x.replace('Reviewed in the United States on ','').replace(',','')
    tt=x.split(' ')
    m,n,p = tt[0],tt[1],tt[2] #n month,n day,p year
    if m=='October' or m=='Oktober' or m=='Oct' or m=='Okt':
        on_date='10-'+n+'-'+p
    elif m=='September' or m=='Sep':
        on_date='09-'+n+'-'+p
    elif m=='June' or m=='Jun':
        on_date='06-'+n+'-'+p
    elif m=='December' or m=='Dezember' or m=='Dec' or m=='Dez':
        on_date='12-'+n+'-'+p
    elif m=='July' or m=='Juli' or m=='Jul':
        on_date='07-'+n+'-'+p
    elif m=='May' or m=='Mai':
        on_date='05-'+n+'-'+p
    elif m=='April' or m=='Apr':
        on_date='04-'+n+'-'+p
    elif m=='February' or m=='Februar' or m=='Feb':
        on_date='02-'+n+'-'+p
    elif m=='March' or m=='März' or m=='Maerz' or m=='Mar':
        on_date='03-'+n+'-'+p
    elif m=='November' or m=='Nov':
        on_date='11-'+n+'-'+p
    elif m=='August' or m=='Aug':
        on_date='08-'+n+'-'+p
    elif m=='January' or m=='Januar' or m=='Jan':
        on_date='01-'+n+'-'+p
    on_date=pd.to_datetime(on_date)
    return on_date

#对分词后的单词还原（复数和时态）
def get_lemma(word):
    lemma=wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
#处理content
def prepare_text_for_lda(n):
    #直接用空格split的话会出现'it.'这样的
    tokens=nltk.word_tokenize(n)
    # 对词进行还原
    tokens=[get_lemma(token) for token in tokens]
    # 补充停用词
    punctuation = [",", ":", ";", ".", "!", "'", '"', "’", "?", "/", "-", "+", "&", "(", ")"]
    stop_words=nltk.corpus.stopwords.words('english')+punctuation
    tokens=[i for i in tokens if i not in stop_words]
    # 进一步可以提取词性（名词、副词）——作业
    return tokens

# import nltk
s=nltk.word_tokenize('6  After one month, it doesn\'t work and the retur.')
print(s)
# lemma=wn.morphy('doing')
# t=nltk.corpus.stopwords.words('english')
# print(t)
