# import os, sys
# import datetime as dt
# import codecs
#
# # from django.contrib.auth import get_user_model
# from django.db import DatabaseError
#
# proj = os.path.dirname(os.path.abspath('manage.py'))
# sys.path.append(proj)
# os.environ["DJANGO_SETTINGS_MODULE"] = "jobscraper.settings"
#
# import django
# django.setup()
#
# from scraping.parsers import work,djinni
# from scraping.models import Vacancy, City, Language
#
# # User = get_user_model()
#
# parsers = (
#     (work, 'https://www.work.ua/jobs-kyiv-python/'),
#     # (dou, 'dou'),
#     (djinni, 'https://djinni.co/jobs/location-kyiv'),
#     # (rabota, 'https://rabota.ua/zapros/python/киев')
# )
# jobs, errors = [], []
#
# city = City.objects.filter(slug='kiev').first()
# language = Language.objects.filter(slug='python').first()
#
# jobs, errors = [], []
# for func, url in parsers:
#     j,e = func(url)
#     jobs += j
#     errors += e
#
# for job in jobs:
#     v = Vacancy(**job, city=city, language=language)
#     v.save()
#
# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()


import os, sys
import datetime as dt
import codecs

# from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from django.db import DatabaseError, IntegrityError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "jobscraper.settings"

import django
django.setup()

from scraping.parsers import work,djinni
from scraping.models import Vacancy, City, Language, Url

User = get_user_model()

parsers = (
    (work, 'work'),
    # (dou, 'dou'),
    (djinni, 'djinni'),
    # (rabota, 'https://rabota.ua/zapros/python/киев')
)

def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst

def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dict:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            url_data = url_dict.get(pair)
            if url_data:
                tmp['url_data'] = url_dict.get(pair)
                urls.append(tmp)
    return urls

settings = get_settings()
url_list = get_urls(settings)


jobs, errors = [], []

for data in url_list:
    for func, key in parsers:
        url = data['url_data'][key]
        j, e = func(url, city=data['city'], language=data['language'])
        jobs += j
        errors += e

for job in jobs:
    v = Vacancy(**job)
    v.save()
    try:
        v.save()
    except DatabaseError:
        pass
    except IntegrityError:
        pass


# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()





#
#
# import asyncio
# import codecs
# import os, sys
# import datetime as dt
#
# from django.contrib.auth import get_user_model
# from django.db import DatabaseError
#
# proj = os.path.dirname(os.path.abspath('manage.py'))
# sys.path.append(proj)
# os.environ["DJANGO_SETTINGS_MODULE"] = "jobscraper.settings"
#
# import django
# django.setup()
#
# from scraping.parsers import *
# from scraping.models import Vacancy, Error, Url
#
# User = get_user_model()
#
# parsers = (
#     (work, 'work'),
#     (dou, 'dou'),
#     (djinni, 'djinni'),
#     (rabota, 'rabota')
# )
# jobs, errors = [], []
#
#
# def get_settings():
#     qs = User.objects.filter(send_email=True).values()
#     settings_lst = set((q['city_id'], q['language_id']) for q in qs)
#     return settings_lst
#
#
# def get_urls(_settings):
#     qs = Url.objects.all().values()
#     url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
#     urls = []
#     for pair in _settings:
#         if pair in url_dict:
#             tmp = {}
#             tmp['city'] = pair[0]
#             tmp['language'] = pair[1]
#             url_data = url_dict.get(pair)
#             if url_data:
#                 tmp['url_data'] = url_dict.get(pair)
#                 urls.append(tmp)
#     return urls
#
#
# async def main(value):
#     func, url, city, language = value
#     job, err = await loop.run_in_executor(None, func, url, city, language)
#     errors.extend(err)
#     jobs.extend(job)
#
# settings = get_settings()
# url_list = get_urls(settings)
#
# loop = asyncio.get_event_loop()
# tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
#              for data in url_list
#              for func, key in parsers]
#
# # for data in url_list:
# #
# #     for func, key in parsers:
# #         url = data['url_data'][key]
# #         j, e = func(url, city=data['city'], language=data['language'])
# #         jobs += j
# #         errors += e
# if tmp_tasks:
#     tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
#     loop.run_until_complete(tasks)
#     loop.close()
#
# for job in jobs:
#     v = Vacancy(**job)
#     try:
#         v.save()
#     except DatabaseError:
#         pass
# if errors:
#     qs = Error.objects.filter(timestamp=dt.date.today())
#     if qs.exists():
#         err = qs.first()
#         err.data.update({'errors': errors})
#         err.save()
#     else:
#         er = Error(data=f'errors:{errors}').save()
#
# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
# # ten_days_ago = dt.date.today() - dt.timedelta(10)
# # Vacancy.objects.filter(timestamp__lte=ten_days_ago).delete()
