from django.shortcuts import render,get_object_or_404
from app01 import models
from .models import Text,Category
import markdown
import re
from pure_pagination import  Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

#
def index(request):

    post_list = models.Text.objects.all() #获取全部文章
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(post_list,5,request=request)

    post_list = p.page(page)

    # title_list=[]
    # excerpt_list =[]
    # for text in all_text:
    #     title=text.title
    #     title_list.append(title)
    # for text in all_text:
    #     excerpt = text.exce
    return render(request,'index.html',{'post_list':post_list,})
# #类视图方法rpt
#     #     excerpt_list.append(excerpt)
#
from  django.views.generic import ListView


# class IndexView(PaginationMixin,ListView):
#       models = Text
#       template_name = 'index.html'
#       context_object_name = 'post_list'
#
# class CategoryView(ListView):
#     models = Text
#     template_name = 'index.html'
#     context_object_name = 'post_list'
#
#     def get_querset(self):
#         cate = get_object_or_404(Category,pk = self.kwargs.get('pk'))
#         return super(CategoryView, self).get_queryset().filter(category=cate)
#


def details(request,pk):

    text=get_object_or_404(Text,pk=pk)
    text.increase_views()  #调用一次阅读量+1
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    text.body = md.convert(text.body)

    m=re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)#，空目录处理

    text.toc = m.group(1) if m is not None else ''  ##动态添加toc属性，即用于目录展示




    return render(request,'single.html',{'TEXT':text
                                        })
    pass
# from django.views.generic import DetailView
# class PostDetailView(DetailView):
#
#     models = Text
#     template_name = 'single.html'
#     context_object_name = 'post'
#
#     def get(self,request,*args,**kwargs):
#         response = super(PostDetailView,self).get(request,*args,**kwargs)
#         self.object.increase_views()
#         return response
#
#
#     def get_object(self, queryset=None):
#
#         post = super().get_object(queryset=None)
#         md = markdown.Markdown(extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         'markdown.extensions.toc',
#         TocExtension(slugify=slugify)
#     ])
#         post.body =md.convert(post.body)
#         m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#
#         post.toc = m.group(1) if m is not None else ''
#         return post






# class ArchiveView(ListView):
#     models = Text
#     template_name = 'index.html'
#     context_object_name = 'post_list'
#     def get_queryset(self):
#         year = self.kwargs.get('year')
#         month = self.kwargs.get('month')
#         return super().get_queryset().filter(created_t_year=year,created_t_momth=month)






def archive(request,year,month):
    print(year)
    print(month)
    text_list=Text.objects.filter(created_t__year=year,
                                         created_t__month=month).order_by('-created_t')
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(text_list, 5, request=request)

    text_list = p.page(page)


    return render(request,'index.html',context={'post_list':text_list})

def category(request,pk):
    cate = get_object_or_404(Category, pk=pk)
    text_list = Text.objects.filter(category=cate).order_by('-created_t')
    print(text_list)
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(text_list, 5, request=request)

    text_list = p.page(page)

    return render(request,'index.html',{'post_list':text_list})

def tag(request,pk):

     # 记得在开始部分导入 Tag 类
    t = get_object_or_404(models.Tags, pk=pk)

    text_list = Text.objects.filter(tags=t).order_by('-created_t')

    try:
         page = request.GET.get('page', 1)
    except PageNotAnInteger:
         page = 1
    p = Paginator(text_list, 5, request=request)

    text_list = p.page(page)
    # tags = models.Tags.objects.filter(pk=pk)
    # text_list = Text.objects.filter(tags=tags).order_by('-created_t')
    return render(request, 'index.html', {'post_list': text_list})

# class TagView(IndexView):
#     def get_queryset(self):
#         t = get_object_or_404(models.Tags,pk=self.kwargs.get('pk'))
#         return super().get_queryset().filter(tags=t)
