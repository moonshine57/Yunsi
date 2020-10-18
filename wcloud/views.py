from django.http import HttpResponse,JsonResponse
from django.template import loader
import io
import uuid
import json

from wcloud.util.generate_wordcloud import generate_wordcloud

from wordcloud import WordCloud

back_coloring_path_prefix = "wcloud\\res\\shape\\" # 设置背景图片路径
font_path = 'wcloud\\res\\simkai.ttf' # 为matplotlib设置中文字体路径没
stopwords_path = 'wcloud\\res\\hit_stopwords.txt' # 停用词词表

def index(request):
    template = loader.get_template('wcloud/index.html')
    return HttpResponse(template.render({}, request))

def result(request):
    text = request.POST['content']
    '''
    wordcloud = WordCloud().generate(text)
    wordcloud.to_file('./wcloud/images/'+filename)
    '''
    imgname = uuid.uuid4().hex+'.png'
    back_coloring_path = back_coloring_path_prefix + '16.png'
    word_frequency = generate_wordcloud(text,imgname,back_coloring_path,font_path,stopwords_path,color_by_backimg=True)
    template = loader.get_template('wcloud/result.html')
    return HttpResponse(template.render({"imgname":imgname,"word_frequency":word_frequency}, request))

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
    back_coloring_path = back_coloring_path_prefix+shape_name
    word_frequency = request.POST.get('word_frequency')
    word_frequency = json.loads(word_frequency)
    word_frequency.pop(0)
    d = {}
    for item in word_frequency:
        item = item.split(',')[:2]
        d[item[0]] = int(item[1])
    imgname = uuid.uuid4().hex+'.png'
    generate_wordcloud(d,imgname,back_coloring_path,font_path,stopwords_path,color_by_backimg=True)

    return JsonResponse({"imgname": imgname})


