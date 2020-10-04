from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud, ImageColorGenerator
import uuid

def generate_wordcloud(text,imgname,back_coloring_path,font_path,stopwords_path,isCN=True,my_words_list=[],color_by_backimg=False):

    '''
    back_coloring_path = "../res/cloud.jpg" # 设置背景图片路径
    text_path = 'txt/lz.txt' #设置要分析的文本路径
    font_path = 'D:\Fonts\simkai.ttf' # 为matplotlib设置中文字体路径没
    stopwords_path = 'stopwords\stopwords1893.txt' # 停用词词表
    my_words_list = ['路明非'] # 在结巴的词库中添加新词
    '''

    back_coloring = imread(back_coloring_path)# 设置背景图片
    # 设置词云属性
    wc = WordCloud(font_path=font_path,  # 设置字体
                background_color="white",  # 背景颜色
                max_words=120,  # 词云显示的最大词数
                mask=back_coloring,  # 设置背景图片
                max_font_size=300,  # 字体最大值
                min_font_size=20,
                random_state=42,
                width=1000, height=860, margin=2,# 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
                collocations=False,
                )

    add_word(my_words_list)
    if isCN:
        text = jiebaclearText(text,stopwords_path)

    # 生成词云, 可以用generate输入全部文本(wordcloud对中文分词支持不好,建议启用中文分词),也可以我们计算好词频后使用generate_from_frequencies函数
    wc.generate(text)
    # wc.generate_from_frequencies(txt_freq)
    # txt_freq例子为[('词a', 100),('词b', 90),('词c', 80)]
    
    if not color_by_backimg:
        # 保存图片
        wc.to_file('wcloud\\images\\'+imgname)
        print(imgname)
        print('保存成功')

    else:
        # 从背景图片生成颜色值
        image_colors = ImageColorGenerator(back_coloring)
        wc.recolor(color_func=image_colors)
        # 保存图片
        wc.to_file('..\\images\\'+imgname)

# 添加自己的词库分词
def add_word(list):
    for items in list:
        jieba.add_word(items)

def jiebaclearText(text,stopwords_path):
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr="/ ".join(seg_list)
    f_stop = open(stopwords_path,encoding = 'utf-8')
    try:
        f_stop_text = f_stop.read( )
    finally:
        f_stop.close( )
    f_stop_seg_list=f_stop_text.split('\n')
    for myword in liststr.split('/'):
        if not(myword.strip() in f_stop_seg_list) and len(myword.strip())>1:
            mywordlist.append(myword)
    return ''.join(mywordlist)