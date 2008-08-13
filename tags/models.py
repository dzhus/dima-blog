from django.db import models
from django.db.models.loading import get_app
from django.conf import settings
from urllib import quote

class Tag(models.Model):
    value = models.CharField(max_length=50)
    norm_value = models.CharField(max_length=50, editable=False)
  
    class Meta:
        ordering=('norm_value','value')
  
    def __unicode__(self):
        return self.value
    
    def save(self):
        tags = get_app('tags')
        from tags.utils import normalize_title
        self.norm_value = normalize_title(self.value)
        super(Tag, self).save()
    
    def get_absolute_url(self):
        def strip_spaces(str):
            return str.replace(" ", "_")
        return settings.TAGS_URL % strip_spaces(self.value)
