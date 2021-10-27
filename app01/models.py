import re

from django.db import models
from django.urls import reverse
from django.utils import timezone
import markdown
from django.contrib.auth.models import User
# Create your models here.

from django.utils.html import strip_tags
#分类表格
from markdown.extensions.toc import TocExtension, slugify


class Category(models.Model):
    name=models.CharField(max_length=32)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


    pass
class Tags(models.Model):
    name=models.CharField(max_length=32)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


#文章表格
class Text(models.Model):
    title = models.CharField('标题',max_length=70)#标题
    body = models.TextField('正文')#正文
    created_t = models.DateTimeField('创建时间',default=timezone.now)#创建时间
    modified_t =models.DateTimeField('修改时间')#最后修改时间
    excerpt = models.CharField('摘要',max_length=300,blank=True)  #摘要
    views = models.PositiveIntegerField(default=0,editable=False) #该类型只允许正整数或0，初始化为0  不允许admin后台编辑
    #一个分类对应多篇文章
    category = models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE)
    #多对多
    tags = models.ManyToManyField(Tags,verbose_name='标签',blank=True)
     #一对多
    auther = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)#

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是
    # django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和
    # Category 类似。
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

        ordering = ['-created_t']
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):#每次保存修改时间
        self.modified_t = timezone.now()

        # 从文本摘取前 54 个字符赋给 excerpt
        # self.excerpt =self.body[:54]

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt
        if self.excerpt is None:
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        # else:
        #     self.excerpt = self.excerpt

        super().save(*args, **kwargs)


    def increase_views(self):
        self.views+=1
        self.save(update_fields=['views'])




