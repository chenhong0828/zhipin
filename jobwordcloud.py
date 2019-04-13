from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
import re
from scipy.misc import imread

path_txt = 'F:\\LearnPython\\zhipin\\zpjob.txt'
# path_txt = 'C:\\Users\\chenhong\\Desktop\\zhipin\\zpjob.txt'
f = open(path_txt, 'r', encoding = 'UTF-8').read()
f = re.compile(r'\n').sub('',f)


# cut_text = " ".join(jieba.cut(f))
cut_text = jieba.lcut(f)

stopwords = [line.strip() for line in open('F:\\LearnPython\\zhipin\\stopwords.txt', 'r', encoding = 'UTF-8').readlines()]
# stopwords = [line.strip() for line in open('C:\\Users\\chenhong\\Desktop\\zhipin\\stopwords.txt', 'r', encoding = 'UTF-8').readlines()]

results = []
for i in cut_text:
    if i not in stopwords:
        results.append(i)

results = " ".join(results)

bg_pic = imread('background.jpg')

wordcloud = WordCloud(mask=bg_pic,
    font_path="C:\\Windows\\Fonts\\simfang.ttf",
    background_color="white", width=1000, height=880).generate(results)

plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

wordcloud.to_file("request.png")