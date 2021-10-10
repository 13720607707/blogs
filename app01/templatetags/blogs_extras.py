from django import template
from ..models import Text,Tags,Category
from django.db.models.aggregates import Count

register = template.Library()
#最新文章模板标签
@register.inclusion_tag('_recent_post.html',takes_context=True)
def show_recent_post(context,num=5):
    return {
        'recent_post_list':Text.objects.all().order_by('-created_t')[:num],
    }
#归档模板标签
@register.inclusion_tag('_archeves.html',takes_context=True)
def show_achieves(context):
    return {
        'date_list':Text.objects.dates('created_t','month',order='DESC')
    }
#分类模板标签
@register.inclusion_tag('_categories.html',takes_context=True)
def show_categories(context):
    cate_list = Category.objects.annotate(num_posts=Count('text')).filter(num_posts__gt=0)#返回全部分类记录，同时计算返回的记录集合中每条记录下的文章数
    return {
        'category_list':cate_list
    }
#标签云模板标签
@register.inclusion_tag('_tags.html', takes_context=True)
def show_tags(context):
    tag_list =Tags.objects.annotate(num_posts=Count('text')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }

