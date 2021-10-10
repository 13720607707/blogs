from django.db import models
from django.utils import timezone
from app01.models import Text
# Create your models here.
class Comment(models.Model):

    name = models.CharField('姓名',max_length=32)
    email = models.EmailField('邮箱')
    url = models.URLField('网址',blank=True)
    text = models.TextField('评论',max_length=50)
    created_t = models.TimeField('创建时间',default=timezone.now)

    post = models.ForeignKey(Text,verbose_name='文章',on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    