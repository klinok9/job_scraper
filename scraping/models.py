import jsonfield
from django.db import models

from scraping.utils import from_cyrillic_to_eng


def default_urls():
    return {"work": "", "rabota": "", "dou": "", "djinni": ""}


class City(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Название населенного пункта',
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Название населенного пункта'
        verbose_name_plural = 'Название населенных пунктов'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Язык программирования',
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='Город', related_name='vacancies')
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()

    def __str__(self):
        return str(self.timestamp)


class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Язык программирования')
    url_data = jsonfield.JSONField(default=default_urls)

    class Meta:
        unique_together = ("city", "language")


# import jsonfield
# from django.db import models
#
# from scraping.utils import from_cyrillic_to_eng
#
#
# def default_urls():
#     return {'worl': '', 'djinni': ''}
#
#
# class City(models.Model):
#     name = models.CharField(max_length=50, verbose_name='Название города', unique=True)
#     slug = models.CharField(max_length=50, blank=True, unique=True)  # blank=True поле может быть пустым
#
#     # меняет в табличке city на 'Название города'
#     class Meta:
#         verbose_name = 'Название города'
#         verbose_name_plural = 'Название городов'
#
#     # меняет City object (1) на название города
#     def __str__(self):
#         return self.name
#
#     # преобразование кирилицы в англ
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = from_cyrillic_to_eng(str(self.name))
#         super().save(*args, **kwargs)
#
#
# class Language(models.Model):
#     name = models.CharField(max_length=50, verbose_name='Название языка программирования', unique=True)
#     slug = models.CharField(max_length=50, blank=True, unique=True)  # blank=True поле может быть пустым
#
#     # меняет в табличке city на 'Название города'
#     class Meta:
#         verbose_name = 'Название языка программирования'
#         verbose_name_plural = 'Название языков программирования'
#
#     # меняет City object (1) на название города
#     def __str__(self):
#         return self.name
#
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = from_cyrillic_to_eng(str(self.name))
#         super().save(*args, **kwargs)
#
#
# class Vacancy(models.Model):
#     url = models.URLField(unique=True)
#     title = models.CharField(max_length=250, verbose_name='Заголвок вакансии')
#     company = models.CharField(max_length=250, verbose_name='Компания')
#     description = models.TextField(verbose_name='Описание вакансии')
#     city = models.ForeignKey('City', on_delete=models.CASCADE,
#                              verbose_name='Город')  # ForeignKey связь между таблицами(отношение многие к одному)
#     language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык программирования')
#     timestamp = models.DateField(auto_now_add=True)  # auto_now_add присваиване даты автомат в базу данных
#
#     class Meta:
#         verbose_name = 'Вакансия'
#         verbose_name_plural = 'Вакансии'
#         ordering = ['timestamp']
#
#     def __str__(self):
#         return self.title
#
#
# class Error(models.Model):
#     timestamp = models.DateField(auto_now_add=True)
#     data = jsonfield.JSONField()
#
#
# class Url(models.Model):
#     city = models.ForeignKey('City', on_delete=models.CASCADE,
#                              verbose_name='Город')  # ForeignKey связь между таблицами(отношение многие к одному)
#     language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык программирования')
#     url_data = jsonfield.JSONField(default=default_urls())
#
#     class Meta:
#         unique_together = ('city', 'language')
