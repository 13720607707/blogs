from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Text,Category,Tags

admin.site.site_header = '蒸汽金鱼的博客'  # 设置header
admin.site.site_title = 'LOVE'          # 设置title

class TextAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_t', 'modified_t', 'category','auther']#表头字段展示
    fields = ['title', 'body', 'excerpt', 'category', 'tags']##表单展示


    def save_model(self, request, obj, form, change):
        obj.auther = request.user
        super().save_model(request, obj, form, change)#表单保存数据库

admin.site.register(Text,TextAdmin)
admin.site.register(Category)
admin.site.register(Tags)