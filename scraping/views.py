from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import Http404
# Create your views here.
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import News, Word, Wordlocation,User,My_lenta
from django.template import loader
from django.shortcuts import get_object_or_404
from .transformation import Transformation
from .gistfile1 import Porter
import nltk
import math
from django.core.paginator import Paginator
from django import forms
from django.http import HttpResponseRedirect
from .forms import UserCForm, LentaForm

nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('russian'))
stop_words.add("в")
stop_words.add("В")
k1 = 2
b = 0.75
avg = 500  # средняя длина документа

from rest_framework import viewsets

from .serializers import NewsSerializer
#from .models import Hero


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('title')
    serializer_class = NewsSerializer


def reg(request):
    if request.method == 'POST':
        form = UserCForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            nuser = User.objects.create_user(new_user.username, new_user.email,new_user.password)

            a = My_lenta.objects.create(lenta_owner=nuser, ria=True, interfax=False,regnum=False,rt=False)
            return redirect( 'scraping:index')
    else:
        form = UserCForm()

    return render(request,"scraping/reg.html", {'form': form })

@login_required
def lenta_sett(request):
    lenta=0
    try:
        lenta=My_lenta.objects.get(lenta_owner=request.user)
    except:
        lenta = My_lenta.objects.create(lenta_owner=request.user,ria=True, interfax=False,regnum=False,rt=False)


    if request.method == 'POST':
        form = LentaForm(request.POST)
        new_lenta=form.save(commit=False)
        My_lenta.objects.filter(lenta_owner=request.user).update(ria=new_lenta.ria,
                                                                 interfax=new_lenta.interfax,
                                                                 regnum=new_lenta.regnum,
                                                                 rt=new_lenta.rt)
            #new_lenta.save()
        return redirect('scraping:lenta')
    else:
        form = LentaForm(instance=lenta)
    return render(request, "scraping/lenta_sett.html", {'form': form})

@login_required
def lenta(request):
    try:
        lenta=My_lenta.objects.get(lenta_owner=request.user)
    except:
        lenta = My_lenta.objects.create(lenta_owner=request.user,ria=True, interfax=False,regnum=False,rt=False)
    news_list_ria=None
    news_list_interfax = None
    news_list_regnum = None
    news_list_rt = None
    news_list = None
    if lenta.ria==True:
        news_list_ria = News.objects.filter(source="РИА новости").order_by('-created_date')
    if lenta.interfax==True:
        news_list_interfax = News.objects.filter(source="Интерфакс").order_by('-created_date')
    if lenta.regnum == True:
        news_list_regnum = News.objects.filter(source="REGNUM").order_by('-created_date')
    if lenta.rt == True:
        news_list_rt = News.objects.filter(source="RT").order_by('-created_date')

    if (news_list_ria!=None):
        news_list = news_list_ria
        if  (news_list_interfax!=None):
            news_list=news_list | news_list_interfax
        if (news_list_regnum != None):
            news_list=news_list |news_list_regnum
        if (news_list_rt != None):
            news_list=news_list | news_list_rt
    elif (news_list_interfax!=None):
        news_list =news_list_interfax
        if (news_list_regnum != None):
            news_list=news_list |news_list_regnum
        if (news_list_rt != None):
            news_list=news_list |news_list_rt
    elif (news_list_regnum != None):
        news_list = news_list_regnum
        if (news_list_rt != None):
            news_list=news_list |news_list_rt
    elif (news_list_rt != None):
        news_list = news_list_rt

    template = loader.get_template('scraping/lenta.html')
    if news_list!=None:
        paginator = Paginator(news_list, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj=None
    context = {

        'page_obj': page_obj
    }
    return HttpResponse(template.render(context, request))





def index(request):
    news_list = News.objects.order_by('-created_date')
    template = loader.get_template('scraping/index.html')
    paginator = Paginator(news_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    zag="Последние новости"
    context = {

        'page_obj': page_obj,
        'num_visits': num_visits,
        'zag':zag
    }
    return HttpResponse(template.render(context, request))


def ria(request):
    news_list = News.objects.filter(source="РИА новости").order_by('-created_date')
    template = loader.get_template('scraping/index.html')
    paginator = Paginator(news_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    zag = "РИА новости"
    context = {

        'page_obj': page_obj,
        'zag': zag
    }
    return HttpResponse(template.render(context, request))


def interfax(request):
    news_list = News.objects.filter(source="Интерфакс").order_by('-created_date')
    template = loader.get_template('scraping/index.html')
    paginator = Paginator(news_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    zag="Интефакс"
    context = {

        'page_obj': page_obj,
        'zag': zag
    }
    return HttpResponse(template.render(context, request))


def regnum(request):
    news_list = News.objects.filter(source="REGNUM").order_by('-created_date')
    template = loader.get_template('scraping/index.html')
    paginator = Paginator(news_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    zag="REGNUM"
    context = {

        'page_obj': page_obj,
        'zag': zag
    }
    return HttpResponse(template.render(context, request))


def rt(request):
    news_list = News.objects.filter(source="RT").order_by('-created_date')
    template = loader.get_template('scraping/index.html')
    paginator = Paginator(news_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    zag="RT"
    context = {

        'page_obj': page_obj,
        'zag': zag
    }
    return HttpResponse(template.render(context, request))


def detail(request, news_id):
    new = get_object_or_404(News, pk=news_id)
    return render(request, 'scraping/detail.html', {'new': new})

def search(request):
    a = request.POST.get('question', False)
    query = Transformation.del_punctuation(str(a))
    query = query.split()
    query_norm = []  # нормализованнный запрос
    for word in query:
        if word in stop_words:
            continue
        query_norm.append(Porter.stem(word))
    # size = {word: 0 for word in query_norm}  # количество
    score = {}
    doc = News.objects.count()  # общее количество документов
    for w in query_norm:
        word_set = Wordlocation.objects.filter(word=w)  # сет словопозиций, количество документов в котором есть слово
        size = word_set.count()
        if size == 0:
            continue# количество документов в которых употребляется слово
        r = doc / size
        idf = math.log(r)
        for word_s in word_set:
            if score.get(word_s.url) is None:
                score[word_s.url] = 0
            chisl =float (word_s.tf * (k1 + 1))
            znam = word_s.d / avg
            znam *= b
            znam += 1
            znam -= b
            znam *= k1
            znam += float(word_s.tf)
            itog = chisl/znam
            itog *= idf
            score[word_s.url] += itog
    list_s = list(score.items())
    list_s.sort(key=lambda i: i[1], reverse=True)
    score1 = dict(list_s)
    n=len(list_s)
    news_list = []
    for s in score1:
        news_list.append(News.objects.get(url=s))

    paginator = Paginator(news_list, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'scraping/search.html', {'a': a, 'news_list': news_list,'n':n})
