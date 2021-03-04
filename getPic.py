from wordcloud import WordCloud
import matplotlib.pyplot as plt
#画词云，输入的是string
def create_word_cloud(f):
    wc = WordCloud(
        font_path="/System/Library/Fonts/STHeiti Medium.ttc",
        # background_color='white',
        max_words=20,
        width=2000,
        height=1200,
        # mask=plt.imread('/Users/zhouya/Downloads/sikao.jpg')  #背景图片
    )
    wordcloud = wc.generate(f)
    # 写词云图片
    wordcloud.to_file("wordcloud.jpg")
    # 显示词云文件
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

