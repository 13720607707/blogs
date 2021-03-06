from django import template
from ..forms import CommentForm

register = template.Library()


@register.inclusion_tag('_form.html', takes_context=True)
def show_comment_form(context, post, form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post,
    }

@register.inclusion_tag('_list.html', takes_context=True)
def show_comments(context, post):
    comment_list = post.comment_set.all().order_by('-created_t')  #等价于 Comment.objects.filter(post=post)
    comment_count = comment_list.count()    #评价数量
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }