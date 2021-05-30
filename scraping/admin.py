from django.contrib import admin
from .models import City, Language, Vacancy, Error, Url

admin.site.register(City)  #регистрация модели в админке
admin.site.register(Language)  #регистрация модели в админке
admin.site.register(Vacancy)  #регистрация модели в админке
admin.site.register(Error)  #регистрация модели в админке
admin.site.register(Url)  #регистрация модели в админке
