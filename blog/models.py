# -*- coding: utf-8 -*-
from django.db import models

from tagging.fields import TagField

#from tags.models import Tag
#from tags.fields import TagsField

class Entry(models.Model):
    title = models.CharField("Заголовок", max_length=128)
    private = models.BooleanField("Личная запись", blank=True)
    text = models.TextField("Текст")
    extra_text = models.TextField("Дополнительный текст", blank=True,
                                  help_text="Данный текст виден только при просмотре отдельной записи.")
    add_date = models.DateTimeField("Дата и время добавления", editable=False, auto_now_add=True)
    edit_date = models.DateTimeField("Дата и время последнего редактирования",
                                     editable=False, null=True, auto_now=True)
    tags = TagField("Теги", blank=True, null=True)
    slug = models.SlugField("Метка", blank=True)

    @models.permalink
    def get_absolute_url(self):
        if self.slug:
            return ('entry_by_slug', [str(self.slug)])
        else:
            return ('entry_by_id', [str(self.id)])

    def __unicode__(self):
        return self.title


    class Admin:
        list_display = ('id','title','add_date', 'comments', 'slug')
        list_display_links = ('title',)
        js = ('../js/tags.gs',)
        search_fields = ('text', 'extra_text', 'title')
        
    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ("-add_date",)

class File(models.Model):
    name = models.CharField("Название", max_length=50)
    description = models.TextField("Описание")
    file = models.FileField("Файл", upload_to="uploads/")
    add_date = models.DateTimeField("Дата и время добавления", editable=False, auto_now_add=True)

    class Admin:
	pass

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __unicode__(self):
        return self.name
