# -*- coding:utf-8 -*-
from django.db import models
from django import oldforms as forms
from django.template import loader, Context
from django.db.models.loading import get_app, get_model
from django.conf import settings

def get_id(model, value):
  if not value:
    return ''
  tags = get_app('tags')
  from tags.utils import normalize_title
  obj_list = model.objects.filter(norm_value__exact=normalize_title(value))
  if len(obj_list):
    return int(obj_list[0].id)
  else:
    obj = model(value=value)
    obj.save()
    return int(obj.id)
    
class TagsFormField(forms.FormField):
  requires_data_list = True
  def __init__(self, field_name, model=None, is_required=False, validator_list=[]):
    self.field_name = field_name
    self.model = model or get_model('tags', 'Tag')
    self.is_required = is_required
    self.max_length = self.model._meta.get_field('value').maxlength
    self.validator_list = [self.isValidLength] + validator_list
    
  def isValidLength(self, data, form):
    for value in data:
      if len(value.decode(settings.DEFAULT_CHARSET)) > self.maxlength:
        raise validators.ValidationError, ngettext("Ensure your text is less than %s character.",
          "Ensure your text is less than %s characters.", self.maxlength) % self.maxlength
    
  def get_validation_errors(self, new_data):
    if new_data.has_key(self.field_name):
      new_data.setlist(self.field_name, [v for v in new_data.getlist(self.field_name) if v != ''])
    return forms.FormField.get_validation_errors(self, new_data)
  
  def convert_post_data(self, new_data):
    forms.FormField.convert_post_data(self, new_data)
    if new_data.has_key(self.field_name):
      new_data.setlist(self.field_name, [get_id(self.model, v) for v in new_data.getlist(self.field_name) if v != ''])
    
  def render(self, data):
    initial_tags = []
    ids = [id for id in data if type(id) == int]
    if ids:
      initial_tags.extend(list(self.model.objects.filter(id__in=ids)))
    strs = [s for s in data if type(s) != int]
    if strs:
      initial_tags.extend(strs)
    template = loader.get_template('tags/tag_widget.html')
    context = Context({
      'field_name': self.field_name,
      'tags': self.model.objects.all(),
      'initial_tags': initial_tags,
      'style_url': hasattr(settings, 'STYLE_URL') and settings.STYLE_URL or '/media/css/',
      'js_url': hasattr(settings, 'JS_URL') and settings.JS_URL or '/media/js/',
      'maxlength': self.maxlength,
    })
    return template.render(context)
    
class TagsField(models.ManyToManyField):
  def get_manipulator_field_objs(self):
    return [TagsFormField]
    
  def prepare_field_objs_and_params(self, manipulator, name_prefix):
    field_objs, params = super(TagsField, self).prepare_field_objs_and_params(manipulator, name_prefix)
    params['model'] = self.rel.to
    return field_objs, params
    
  def flatten_data(self, follow, obj=None):
    new_data = {}
    if obj:
      new_data[self.name] = [int(instance.id) for instance in getattr(obj, self.name).all()]
    return new_data
