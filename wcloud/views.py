from django.http import HttpResponse,JsonResponse
from django.template import loader
import io
import uuid

from wcloud.util.generate_wordcloud import generate_wordcloud

from wordcloud import WordCloud

back_coloring_path = "wcloud\\res\\cloud.jpg" # 设置背景图片路径
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
    word_frequency = generate_wordcloud(text,imgname,back_coloring_path,font_path,stopwords_path)
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
    return JsonResponse({"msg": "ok"})


