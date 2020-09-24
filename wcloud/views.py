from django.http import HttpResponse
from django.template import loader
import io
import uuid

from wordcloud import WordCloud

def index(request):
    template = loader.get_template('wcloud/index.html')
    return HttpResponse(template.render({}, request))

def result(request):
    text = request.POST['content']
    wordcloud = WordCloud().generate(text)
    filename = uuid.uuid4().hex+'.png'
    wordcloud.to_file('./wcloud/images/'+filename)
    template = loader.get_template('wcloud/result.html')
    return HttpResponse(template.render({"filename":filename}, request))

def download(request):
    filename = request.GET.get('filename')
    f = open('./wcloud/images/'+filename,'rb')
    response = HttpResponse(f)
    f.close()
    response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="wordcloud.png"' 
    return response

