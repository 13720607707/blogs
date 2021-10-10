

from django import forms
from .models import Comment
#自动为我们创建常规的表单代码  HTML
##自带的表单功能
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment                           #这个表单对应的数据库模型是Comment类

        fields = ['name','email','url','text']    #表单需要显示的字段



