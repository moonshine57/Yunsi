from django.http import HttpResponse,JsonResponse
from django.template import loader
from .forms import TextForm
from django.contrib import messages
import io
import uuid
import json

from wcloud.util.generate_wordcloud import generate_wordcloud
from django.shortcuts import render

from wordcloud import WordCloud

back_coloring_path_prefix = "wcloud\\res\\shape\\" # 设置背景图片路径
font_path_prefix = 'wcloud\\res\\' # 为matplotlib设置中文字体路径没
stopwords_path = 'wcloud\\res\\hit_stopwords.txt' # 停用词词表

'''
def index(request):
    template = loader.get_template('wcloud/index.html')
    return HttpResponse(template.render({}, request))
'''
'''
def result(request):
    text = request.POST['content']    
    imgname = uuid.uuid4().hex+'.png'
    back_coloring_path = back_coloring_path_prefix + '1.png'
    font_path = font_path_prefix + 'simkai.ttf'
    try:
        word_frequency = generate_wordcloud(text,imgname,back_coloring_path,font_path,stopwords_path,color_by_backimg=False)
    except ValueError:
        template = loader.get_template('wcloud/index.html')
        return HttpResponse(template.render({'script':"alert",'wrong':'输入内容无效'}))
    template = loader.get_template('wcloud/result.html')
    return HttpResponse(template.render({"imgname":imgname,"word_frequency":word_frequency}, request))
'''
def index(request):
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            imgname = uuid.uuid4().hex+'.png'
            back_coloring_path = back_coloring_path_prefix + '1.png'
            font_path = font_path_prefix + 'simkai.ttf'
            try:
                word_frequency = generate_wordcloud(text,imgname,back_coloring_path,font_path,stopwords_path,color_by_backimg=False)
                template = loader.get_template('wcloud/result.html')
                return HttpResponse(template.render({"imgname":imgname,"word_frequency":word_frequency}, request))
            except ValueError:
                messages.info(request, '输入的文本无效，请重新输入')
                return render(request,'wcloud/index.html',{'form':form})
    else:
        form = TextForm(initial={'text':'''    盼望着，盼望着，东风来了，春天的脚步近了。
    一切都像刚睡醒的样子，欣欣然张开了眼。山朗润起来了，水涨起来了，太阳的脸红起来了。
    小草偷偷地从土里钻出来，嫩嫩的，绿绿的。园子里，田野里，瞧去，一大片一大片满是的。坐着，躺着，打两个滚，踢几脚球，赛几趟跑，捉几回迷藏。风轻悄悄的，草软绵绵的。
    桃树、杏树、梨树，你不让我，我不让你，都开满了花赶趟儿。红的像火，粉的像霞，白的像雪。花里带着甜味儿；闭了眼，树上仿佛已经满是桃儿、杏儿、梨儿。花下成千成百的蜜蜂嗡嗡地闹着，大小的蝴蝶飞来飞去。野花遍地是：杂样儿，有名字的，没名字的，散在草丛里，像眼睛，像星星，还眨呀眨的。
    “吹面不寒杨柳风”，不错的，像母亲的手抚摸着你。风里带来些新翻的泥土的气息，混着青草味儿，还有各种花的香，都在微微润湿的空气里酝酿。鸟儿将窠巢安在繁花嫩叶当中，高兴起来了，呼朋引伴地卖弄清脆的喉咙，唱出宛转的曲子，与轻风流水应和着。牛背上牧童的短笛，这时候也成天在嘹亮地响。
    雨是最寻常的，一下就是三两天。可别恼。看，像牛毛，像花针，像细丝，密密地斜织着，人家屋顶上全笼着一层薄烟。树叶儿却绿得发亮，小草儿也青得逼你的眼。傍晚时候，上灯了，一点点黄晕的光，烘托出一片安静而和平的夜。乡下去，小路上，石桥边，有撑起伞慢慢走着的人，地里还有工作的农民，披着蓑，戴着笠的。他们的草屋，稀稀疏疏的在雨里静默着。
    天上风筝渐渐多了，地上孩子也多了。城里乡下，家家户户，老老小小，他们也赶趟儿似的，一个个都出来了。舒活舒活筋骨，抖擞抖擞精神，各做各的一份事去。“一年之计在于春”，刚起头儿，有的是工夫，有的是希望。
    春天像刚落地的娃娃，从头到脚都是新的，它生长着。
    春天像小姑娘，花枝招展的，笑着，走着。
    春天像健壮的青年，有铁一般的胳膊和腰脚，他领着我们上前去'''})
    return render(request,'wcloud/index.html',{'form':form})
        


def download(request):
    imgname = request.GET.get('imgname')
    f = open('wcloud\\images\\'+imgname,'rb')
    response = HttpResponse(f)
    f.close()
    response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="wordcloud.png"' 
    return response

def regenerate(request):
    shape_name = request.POST.get('shapeName')
    word_color = request.POST.get('wordColor')
    bg_color = request.POST.get('bgColor')
    rotate = float(request.POST.get('rotate'))
    wordnum = int(request.POST.get('wordnum'))
    font = request.POST.get('font')
    font_path = font_path_prefix + font
    back_coloring_path = back_coloring_path_prefix+shape_name
    word_frequency = request.POST.get('word_frequency')
    word_frequency = json.loads(word_frequency)
    word_frequency.pop(0)
    d = {}
    for item in word_frequency:
        item = item.split(',')[:2]
        d[item[0]] = int(item[1])
    imgname = uuid.uuid4().hex+'.png'
    generate_wordcloud(d,imgname,back_coloring_path,font_path,stopwords_path,color_by_backimg=False,word_color=word_color,bg_color=bg_color,rotate=rotate,wordnum=wordnum)

    return JsonResponse({"imgname": imgname})


