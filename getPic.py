import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#画词云，输入的是string
def create_word_cloud(f):
    wc = WordCloud(
        # font_path="/System/Library/Fonts/STHeiti Medium.ttc",
        # background_color='white',
        max_words=30,
        width=2000,
        height=1200,
        collocations=False
        # mask=plt.imread('/Users/zhouya/Downloads/sikao.jpg')  #背景图片
    )
    wordcloud = wc.generate(f)
    # 写词云图片
    wordcloud.to_file("wordcloud.jpg")
    # 显示词云文件
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

# l=['a','a','b','a','a','c']
# l=['好的','好的','啊','啊','好的','啊']
# print(" ".join(l))
# s=" ".join(l)
text='你好李焕英你好贾玲你好张小斐'
s=jieba.cut(text)
print(" ".join(s))
# wc = WordCloud(
# # font_path="/System/Library/Fonts/STHeiti Medium.ttc",
# # collocations=False
# )
wc=WordCloud()
wordcloud = wc.generate(" ".join(s))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()