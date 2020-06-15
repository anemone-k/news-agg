from django.core.management.base import BaseCommand

from urllib.request import urlopen
from bs4 import BeautifulSoup
from scraping.models import News

import re

import requests


import datetime


def date_ria(date):
    date = date.split()
    time = date[0]
    date2 = date[1]
    time = time.split(':')
    hour = int(time[0])
    minute = int(time[1])
    date2 = date2.split('.')
    day = int(date2[0])
    month = int(date2[1])
    year = int(date2[2])
    date = datetime.datetime(year, month, day, hour, minute, 0, 0)
    return date


def date_interfax(date):
    date = date.split('T')
    time = date[1]
    date2 = date[0]
    time = time.split(':')
    hour = int(time[0])
    minute = int(time[1])
    date2 = date2.split('-')
    day = int(date2[2])
    month = int(date2[1])
    year = int(date2[0])
    date = datetime.datetime(year, month, day, hour, minute, 0, 0)
    return date


def date_rt(date):
    date = date.split()
    time = date[1]
    date2 = date[0]
    time = time.split(':')
    hour = int(time[0])
    minute = int(time[1])
    date2 = date2.split('-')
    day = int(date2[2])
    month = int(date2[1])
    year = int(date2[0])
    date = datetime.datetime(year, month, day, hour, minute, 0, 0)
    return date


class Command(BaseCommand):
    help = "collect news"

    # определяем логику команд
    def handle(self, *args, **options):


        # собираем html
        # РИА новости
        source = 'РИА новости'
        html = urlopen('https://ria.ru')

        # преобразуем в soup-объект
        soup = BeautifulSoup(html, 'html.parser')

        # собираем все посты без картинок
        # postings = soup.find_all("div", class_="cell-list__list")

        postings = soup.find_all("div", class_="cell-list__item m-no-image")

        for p in postings:
            url = p.find('a', class_='cell-list__item-link color-font-hover-only')['href']
            # print(url)
            title = p.find("span", class_="cell-list__item-title").text
            # print(title)
            try:
                sub_html = urlopen(url)
                soup2 = BeautifulSoup(sub_html, 'html.parser')
                text = soup2.find_all("div", class_="article__text")
                data = ''
                for i in text:
                    data += i.text
                date = soup2.find("div", class_="article__info-date").text
                date = date_ria(date)
            except:
                continue
            # print(data)'

            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))
            except:
                print('%s already exists' % (title,))

        # собираем все посты из большого списка

        postings = soup.find_all("div", class_="cell-author__item")

        for p in postings:
            url = p.find('a', class_='cell-author__item-link color-font-hover-only')['href']
            # print(url)
            title = p.find("span", class_="cell-author__item-title").text
            # print(title)
            sub_html = urlopen(url)
            soup2 = BeautifulSoup(sub_html, 'html.parser')
            text = soup2.find_all("div", class_="article__text")
            data = ''
            for i in text:
                data += i.text
            date = soup2.find("div", class_="article__info-date").text
            date = date_ria(date)
            # print(data)'

            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))

            except:
                print('%s already exists' % (title,))

            # собираем все посты с картинками
        postings = soup.find_all("div", class_="cell cell-main-photo")
        for p in postings:
            url = p.find('a', class_='cell-main-photo__link')['href']
            # print(url)
            title = p.find("span", class_="cell-main-photo__title").text
            # print(title)
            sub_html = urlopen(url)
            soup2 = BeautifulSoup(sub_html, 'html.parser')
            text = soup2.find_all("div", class_="article__text")
            data = ''
            for i in text:
                data += i.text
            date = soup2.find("div", class_="article__info-date").text
            date = date_ria(date)
            # print(data)'

            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))
            except:
                print('%s already exists' % (title,))
        # посты про корону

        postings = soup.find_all("a", class_="cell-supertag__item")
        for p in postings:
            url = p.get('href')
            # print(url)
            title = p.find("span", class_="cell-supertag__item-text").text
            # print(title)
            sub_html = urlopen(url)
            soup2 = BeautifulSoup(sub_html, 'html.parser')
            text = soup2.find_all("div", class_="article__text")
            data = ''
            for i in text:
                data += i.text
            date = soup2.find("div", class_="article__info-date").text
            date = date_ria(date)
            # print(data)'

            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))

            except:
                print('%s already exists' % (title,))

        source = 'Интерфакс'
        html = urlopen('https://interfax.ru')

        # преобразуем в soup-объект
        soup = BeautifulSoup(html, 'html.parser')

        # главные новости

        postings = soup.find("div", class_="newsmain")
        interfax = 'https://interfax.ru'
        postings = postings.find_all("a")

        for p in postings:
            s = p.get('href')
            if s.find('sport-interfax') != -1:
                url = p.get('href')
            else:
                url = interfax + p.get('href')
            # print(url)
            title = p.text

            # print(title)
            sub_html = urlopen(url)
            soup2 = BeautifulSoup(sub_html, 'html.parser')
            text = soup2.find("article")
            if text == None:
                continue
            text = text.find_all('p')
            data = ''
            for i in text:
                data += i.text
            date = soup2.find('time')
            date = date.get('datetime')
            date = date_interfax(date)
            # print(data)'

            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))

            except:
                print('%s already exists' % (title,))
        # интерфакс лента

        postings = soup.find("div", class_="timeline")
        postings = postings.find_all("a")

        for p in postings:
            '''
            if re.match(r'/\w+/\s+', p.get('href')):
                url = interfax+p.get('href')
            else:url=p.get('href')
            '''
            s = p.get('href')
            if s.find('sport-interfax') != -1:
                url = p.get('href')
            else:
                url = interfax + p.get('href')
            # print(url)
            title = p.text
            if title == None:
                continue
            # print(title)
            sub_html = urlopen(url)
            soup2 = BeautifulSoup(sub_html, 'html.parser')
            text = soup2.find("article")
            if text == None:
                continue
            text = text.find_all('p')
            data = ''
            for i in text:
                data += i.text
            date = soup2.find('time')
            date = date.get('datetime')
            date = date_interfax(date)
            # print(data)'

            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))

            except:
                print('%s already exists' % (title,))

        # Регнум

        source = 'REGNUM'
        html = urlopen('https://regnum.ru')

        # преобразуем в soup-объект
        soup = BeautifulSoup(html, 'html.parser')

        # собираем все просто посты
        # postings = soup.find_all("div", class_="cell-list__list")

        postings = soup.find_all("a", class_="news-container-item")

        for p in postings:
            url = p.get('href')
            if url == None:
                continue
            date = p.get('data-time')
            date = datetime.datetime.fromtimestamp(int(date))
            title = p.find('span', class_='news-container-item__article-header').text
            if title.find('все новости') != -1:
                continue
            if title.find('трансляция') != -1:
                continue
            # print(title)
            r = requests.get(url)
            encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
            soup2 = BeautifulSoup(r.content, from_encoding=encoding, features="html.parser")

            soup3 = str(''.join(map(str, soup2)))

            soup3 = BeautifulSoup(soup3, 'html.parser')
            text = soup3.find("div", class_='article-text')
            if text == None:
                continue
            text = text.find_all('p')
            data = ''
            for i in text:
                data += i.text

            # print(data)'

            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))

            except:
                print('%s already exists' % (title,))
        # регнум федеральные

        postings = soup.find_all("a", class_="news-container-item news-container-item--federal")

        for p in postings:
            url = p.get('href')
            if url == None:
                continue
            date = p.get('data-time')
            date = datetime.datetime.fromtimestamp(int(date))
            title = p.find('span', class_='news-container-item__article-header').text
            if title.find('все новости') != -1:
                continue
            if title.find('трансляция') != -1:
                continue
            # print(title)
            r = requests.get(url)
            encoding = r.encoding if 'charset' in r.headers.get('content-type', '').lower() else None
            soup2 = BeautifulSoup(r.content, from_encoding=encoding, features="html.parser")

            soup3 = str(''.join(map(str, soup2)))

            soup3 = BeautifulSoup(soup3, 'html.parser')
            text = soup3.find("div", class_='article-text')
            if text == None:
                continue
            text = text.find_all('p')
            data = ''
            for i in text:
                data += i.text

            # print(data)'

            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))

            except:
                print('%s already exists' % (title,))

        # RT

        # RT главные
        source = 'RT'
        html = urlopen('https://russian.rt.com')
        rt = 'https://russian.rt.com'
        soup = BeautifulSoup(html, 'html.parser')

        main1 = soup.find("div", class_="rows__column rows__column_main_promobox")
        main1 = main1.find_all('a')
        for p in main1:
            if re.match(r'/\S+/\S+[^#]', p.get('href')):
                url = rt + p.get('href')

                sub_html = urlopen(url)
                soup2 = BeautifulSoup(sub_html, 'html.parser')
                title = soup2.find("h1", class_='article__heading article__heading_article-page')
                if title == None:
                    title = soup2.find("h1", class_='article__heading')
                if title != None:
                    title = title.text
                    data = soup2.find('div',
                                      class_="article__summary article__summary_article-page js-mediator-article")
                    if data == None:
                        data = soup2.find('div', class_="article__summary")
                    if data != None:
                        data = data.text
                        text = soup2.find('div', class_='article__text article__text_article-page js-mediator-article')
                        if text != None:
                            text = text.find_all('p')
                        if text != None:
                            for p in text:
                                data = data + ' '
                                data = data + p.text

                date = soup2.find('time', class_="date")['datetime']
                date = str(date)
                date = date_rt(date)

            if (title == None) & (data == None):
                continue
            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))
            except:
                print('%s already exists' % (title,))

        # RT лента
        lenta = soup.find_all("li", class_="listing__column listing__column_main-news")
        for l in lenta:
            url = rt + l.find('a')['href']

            sub_html = urlopen(url)
            soup2 = BeautifulSoup(sub_html, 'html.parser')
            title = soup2.find("h1", class_='article__heading article__heading_article-page')
            if title == None:
                title = soup2.find("h1", class_='article__heading')
            if title != None:
                title = title.text
                data = soup2.find('div', class_="article__summary article__summary_article-page js-mediator-article")
                if data == None:
                    data = soup2.find('div', class_="article__summary")
                if data != None:
                    data = data.text
                    text = soup2.find('div', class_='article__text article__text_article-page js-mediator-article')
                    if text != None:
                        text = text.find_all('p')
                    if text != None:
                        for p in text:
                            data = data + ' '
                            data = data + p.text

            date = soup2.find('time', class_="date")['datetime']
            date = str(date)
            date = date_rt(date)

            if (title == None) & (data == None):
                continue
            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))

            except:
                print('%s already exists' % (title,))

        # RT 3 колонки

        main1 = soup.find_all("div", class_="rows__column rows__column_three-three-three-one rows__column_main-promo")
        for m in main1:
            main2 = m.find_all('a')

            for p in main2:

                if re.match(r'/\S+/\S+[^#]', p.get('href')):
                    url = rt + p.get('href')

                    sub_html = urlopen(url)
                    soup2 = BeautifulSoup(sub_html, 'html.parser')
                    title = soup2.find("h1", class_='article__heading article__heading_article-page')
                    if title == None:
                        title = soup2.find("h1", class_='article__heading')
                    if title != None:
                        title = title.text
                        data = soup2.find('div',
                                          class_="article__summary article__summary_article-page js-mediator-article")
                        if data == None:
                            data = soup2.find('div', class_="article__summary")
                        if data != None:
                            data = data.text
                            text = soup2.find('div',
                                              class_='article__text article__text_article-page js-mediator-article')
                            if text != None:
                                text = text.find_all('p')
                            if text != None:
                                for p in text:
                                    data = data + ' '
                                    data = data + p.text

                    date = soup2.find('time', class_="date")['datetime']
                    date = str(date)
                    date = date_rt(date)

                if (title == None) & (data == None):
                    continue
                try:
                    # сохраняем в базе данных
                    a = News.objects.create(
                        url=url,
                        title=title,
                        data=data,
                        source=source,
                        created_date=date)
                    print('%s added' % (title,))

                except:
                    print('%s already exists' % (title,))
        # RT самые читаемые

        flex = soup.find("div", class_="listing__content listing__content_top-news")

        flex = flex.find_all("div", class_="card__heading card__heading_top-news")

        for l in flex:
            l = l.find('a')
            url = rt + l.get('href')

            sub_html = urlopen(url)
            soup2 = BeautifulSoup(sub_html, 'html.parser')
            title = soup2.find("h1", class_='article__heading article__heading_article-page')
            if title == None:
                title = soup2.find("h1", class_='article__heading')
            if title != None:
                title = title.text
                data = soup2.find('div', class_="article__summary article__summary_article-page js-mediator-article")
                if data == None:
                    data = soup2.find('div', class_="article__summary")
                if data != None:
                    data = data.text
                    text = soup2.find('div', class_='article__text article__text_article-page js-mediator-article')
                    if text != None:
                        text = text.find_all('p')
                    if text != None:
                        for p in text:
                            data = data + ' '
                            data = data + p.text

            date = soup2.find('time', class_="date")['datetime']
            date = str(date)
            date = date_rt(date)

            if (title == None) & (data == None):
                continue
            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))

            except:
                print('%s already exists' % (title,))
        # новости в мире

        flex = soup.find("div",
                         class_="rows__column rows__column_three-three-two-one rows__column_main rows__column_world")

        flex = flex.find("ul", class_="listing__rows listing__rows_main-section")
        flex = flex.find_all('a', class_="link link_color")

        for l in flex:
            url = rt + l.get('href')

            sub_html = urlopen(url)
            soup2 = BeautifulSoup(sub_html, 'html.parser')
            title = soup2.find("h1", class_='article__heading article__heading_article-page')
            if title == None:
                title = soup2.find("h1", class_='article__heading')
            if title != None:
                title = title.text
                data = soup2.find('div', class_="article__summary article__summary_article-page js-mediator-article")
                if data == None:
                    data = soup2.find('div', class_="article__summary")
                if data != None:
                    data = data.text
                    text = soup2.find('div', class_='article__text article__text_article-page js-mediator-article')
                    if text != None:
                        text = text.find_all('p')
                    if text != None:
                        for p in text:
                            data = data + ' '
                            data = data + p.text

            date = soup2.find('time', class_="date")['datetime']
            date = str(date)
            date = date_rt(date)

            if (title == None) & (data == None):
                continue
            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))

            except:
                print('%s already exists' % (title,))

        # рт эксклюзив
        flex = soup.find("div", class_="rows__column rows__column_three-three-two-one rows__column_main")

        flex = flex.find("div", class_="listing__content listing__content_main-section")
        flex = flex.find_all('a', class_="link link_color")

        for l in flex:
            url = rt + l.get('href')

            sub_html = urlopen(url)
            soup2 = BeautifulSoup(sub_html, 'html.parser')
            title = soup2.find("h1", class_='article__heading article__heading_article-page')
            if title == None:
                title = soup2.find("h1", class_='article__heading')
            if title != None:
                title = title.text
                data = soup2.find('div', class_="article__summary article__summary_article-page js-mediator-article")
                if data == None:
                    data = soup2.find('div', class_="article__summary")
                if data != None:
                    data = data.text
                    text = soup2.find('div', class_='article__text article__text_article-page js-mediator-article')
                    if text != None:
                        text = text.find_all('p')
                    if text != None:
                        for p in text:
                            data = data + ' '
                            data = data + p.text

            if (title == None) & (data == None):
                continue
            date = soup2.find('time', class_="date")
            if date == None:
                continue
            date = date.get('datetime')
            date = str(date)
            date = date_rt(date)
            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))

            except:
                print('%s already exists' % (title,))

        flex = soup.find("div", class_="listing__content listing__content_top-news")

        flex = flex.find_all("div", class_="card__heading card__heading_top-news")

        for l in flex:
            l = l.find('a')
            url = rt + l.get('href')

            sub_html = urlopen(url)
            soup2 = BeautifulSoup(sub_html, 'html.parser')
            title = soup2.find("h1", class_='article__heading article__heading_article-page')
            if title == None:
                title = soup2.find("h1", class_='article__heading')
            if title != None:
                title = title.text
                data = soup2.find('div', class_="article__summary article__summary_article-page js-mediator-article")
                if data == None:
                    data = soup2.find('div', class_="article__summary")
                if data != None:
                    data = data.text
                    text = soup2.find('div', class_='article__text article__text_article-page js-mediator-article')
                    if text != None:
                        text = text.find_all('p')
                    if text != None:
                        for p in text:
                            data = data + ' '
                            data = data + p.text

            date = soup2.find('time', class_="date")['datetime']
            date = str(date)
            date = date_rt(date)

            if (title == None) & (data == None):
                continue
            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))

            except:
                print('%s already exists' % (title,))
        # новости в мире

        flex = soup.find("div",
                         class_="rows__column rows__column_three-three-two-one rows__column_main rows__column_world")

        flex = flex.find("ul", class_="listing__rows listing__rows_main-section")
        flex = flex.find_all('a', class_="link link_color")

        for l in flex:
            url = rt + l.get('href')

            sub_html = urlopen(url)
            soup2 = BeautifulSoup(sub_html, 'html.parser')
            title = soup2.find("h1", class_='article__heading article__heading_article-page')
            if title == None:
                title = soup2.find("h1", class_='article__heading')
            if title != None:
                title = title.text
                data = soup2.find('div', class_="article__summary article__summary_article-page js-mediator-article")
                if data == None:
                    data = soup2.find('div', class_="article__summary")
                if data != None:
                    data = data.text
                    text = soup2.find('div', class_='article__text article__text_article-page js-mediator-article')
                    if text != None:
                        text = text.find_all('p')
                    if text != None:
                        for p in text:
                            data = data + ' '
                            data = data + p.text

            date = soup2.find('time', class_="date")['datetime']
            date = str(date)
            date = date_rt(date)

            if (title == None) & (data == None):
                continue
            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))

            except:
                print('%s already exists' % (title,))

        # рт эксклюзив
        flex = soup.find("div", class_="rows__flex rows__flex_main-sport")
        flex = flex.find_all('a', class_="link link_color")

        for l in flex:
            url = rt + l.get('href')

            sub_html = urlopen(url)
            soup2 = BeautifulSoup(sub_html, 'html.parser')
            title = soup2.find("h1", class_='article__heading article__heading_article-page')
            if title == None:
                title = soup2.find("h1", class_='article__heading')
            if title != None:
                title = title.text
                data = soup2.find('div', class_="article__summary article__summary_article-page js-mediator-article")
                if data == None:
                    data = soup2.find('div', class_="article__summary")
                if data != None:
                    data = data.text
                    text = soup2.find('div', class_='article__text article__text_article-page js-mediator-article')
                    if text != None:
                        text = text.find_all('p')
                    if text != None:
                        for p in text:
                            data = data + ' '
                            data = data + p.text

            if (title == None) & (data == None):
                continue
            date = soup2.find('time', class_="date")
            if date == None:
                continue
            date = date.get('datetime')
            date = str(date)
            date = date_rt(date)
            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))
            except:
                print('%s already exists' % (title,))

        flex = soup.find("div",
                         class_="rows__column rows__column_three-three-three-one rows__column_main rows__column_nopolitics")

        flex = flex.find("div", class_="listing__content")
        flex = flex.find_all('a', class_="link link_color")

        for l in flex:
            url = rt + l.get('href')

            sub_html = urlopen(url)
            soup2 = BeautifulSoup(sub_html, 'html.parser')
            title = soup2.find("h1", class_='article__heading article__heading_article-page')
            if title == None:
                title = soup2.find("h1", class_='article__heading')
            if title != None:
                title = title.text
                data = soup2.find('div', class_="article__summary article__summary_article-page js-mediator-article")
                if data == None:
                    data = soup2.find('div', class_="article__summary")
                if data != None:
                    data = data.text
                    text = soup2.find('div', class_='article__text article__text_article-page js-mediator-article')
                    if text != None:
                        text = text.find_all('p')
                    if text != None:
                        for p in text:
                            data = data + ' '
                            data = data + p.text

            if (title == None) & (data == None):
                continue
            date = soup2.find('time', class_="date")
            if date == None:
                continue
            date = date.get('datetime')
            date = str(date)
            date = date_rt(date)
            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))

            except:
                print('%s already exists' % (title,))
        flex = soup.find("div", class_="rows__column rows__column_three-three-three-one rows__column_main_science")

        flex = flex.find("div", class_="listing__content")
        flex = flex.find_all('a', class_="link link_color")

        for l in flex:
            url = rt + l.get('href')

            sub_html = urlopen(url)
            soup2 = BeautifulSoup(sub_html, 'html.parser')
            title = soup2.find("h1", class_='article__heading article__heading_article-page')
            if title == None:
                title = soup2.find("h1", class_='article__heading')
            if title != None:
                title = title.text
                data = soup2.find('div', class_="article__summary article__summary_article-page js-mediator-article")
                if data == None:
                    data = soup2.find('div', class_="article__summary")
                if data != None:
                    data = data.text
                    text = soup2.find('div', class_='article__text article__text_article-page js-mediator-article')
                    if text != None:
                        text = text.find_all('p')
                    if text != None:
                        for p in text:
                            data = data + ' '
                            data = data + p.text

            if (title == None) & (data == None):
                continue
            date = soup2.find('time', class_="date")
            if date == None:
                continue
            date = date.get('datetime')
            date = str(date)
            date = date_rt(date)
            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))

            except:
                print('%s already exists' % (title,))
        flex = soup.find("div", class_="rows__column rows__column_three-three-three-one rows__column_main")

        flex = flex.find("div", class_="listing__content")
        flex = flex.find_all('a', class_="link link_color")

        for l in flex:
            url = rt + l.get('href')

            sub_html = urlopen(url)
            soup2 = BeautifulSoup(sub_html, 'html.parser')
            title = soup2.find("h1", class_='article__heading article__heading_article-page')
            if title == None:
                title = soup2.find("h1", class_='article__heading')
            if title != None:
                title = title.text
                data = soup2.find('div', class_="article__summary article__summary_article-page js-mediator-article")
                if data == None:
                    data = soup2.find('div', class_="article__summary")
                if data != None:
                    data = data.text
                    text = soup2.find('div', class_='article__text article__text_article-page js-mediator-article')
                    if text != None:
                        text = text.find_all('p')
                    if text != None:
                        for p in text:
                            data = data + ' '
                            data = data + p.text

            if (title == None) & (data == None):
                continue
            date = soup2.find('time', class_="date")
            if date == None:
                continue
            date = date.get('datetime')
            date = str(date)
            date = date_rt(date)
            try:
                # сохраняем в базе данных
                a = News.objects.create(
                    url=url,
                    title=title,
                    data=data,
                    source=source,
                    created_date=date)
                print('%s added' % (title,))

            except:
                print('%s already exists' % (title,))

        self.stdout.write('news complete')
