from django.urls import path

from . import views
app_name = 'scraping'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:news_id>/', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('lenta_sett/', views.lenta_sett, name='lenta_sett'),
    path('lenta/', views.lenta, name='lenta'),
    path('reg/', views.reg, name='reg'),
    path('ria/', views.ria, name='ria'),

    path('interfax/', views.interfax, name='interfax'),
    path('regnum/', views.regnum, name='regnum'),
    path('rt/', views.rt, name='rt'),
]
'''path('search/', views.search, name='search'),'''