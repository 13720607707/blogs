#批量生成数据的脚本


import os
import pathlib
import random
import sys
import django
import faker
from datetime import timedelta
from django.utils import timezone
# 将项目根目录添加到python的模块搜索路径中

back = os.path.dirname

BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE","blogs.settings")
    django.setup()
    from app01.models import Category,Text,Tags
    from comments.models import Comment
    from django.contrib.auth.models import User


    #这是整个脚本最为重要的部分。首先设置 DJANGO_SETTINGS_MODULE 环境变量，
    # 这将指定 django 启动时使用的配置文件，然后运行 django.setup() 启动 django。这是关键步骤，
    # 只有在 django 启动后，我们才能使用 django 的 ORM 系统。django 启动后，就可以导入各个模型，
    # 以便创建数据。

    print('clean database')
    Text.objects.all().delete()
    Category.objects.all().delete()
    Tags.objects.all().delete()
    Comment.objects.all().delete()
    User.objects.all().delete()


    print('create a blog user')
    user  =User.objects.create_superuser('admin','admin@hellogithub.com','admin')

    category_list = ['python笔记','开源项目','工具资源','程序员生活生涯','test category']
    tags_list = ['django','python','Docker','java','test tag']
    a_year_ago = timezone.now() - timedelta(days=365)

    print('create category and tag')
    for cate in category_list:
        Category.objects.create(name=cate)

    for tag in tags_list:
        Tags.objects.create(name=tag)

    print('create a markdown sample post')
    Text.objects.create(  title='Markdown 与代码高亮测试',
        body=pathlib.Path(BASE_DIR).joinpath('scripts', 'md.sample').read_text(encoding='utf-8'),
        category=Category.objects.create(name='Markdown测试'),
        auther=user,
    )



    print('create some faked post published within the post year')
    fake = faker.Faker()# 首先实例化一个fake对象，然后可以在脚本中使用这个实例的一些方法生成需要的数据
    for _ in range(100):
        tags = Tags.objects.order_by('?')# ？表示随机排序
        tag1 = tags.first()
        tag2 = tags.last()
        cate = Category.objects.order_by('?').first()
        #-1y 一年前   终止日期为当前
        created_time = fake.date_time_between(start_date = '-1y',end_date='now',tzinfo=timezone.get_current_timezone())
        post = Text.objects.create(
            title=fake.sentence().rstrip('.'),
            body='\n\n'.join(fake.paragraphs(10)),#生成10个段落，以列表形式返回  换行符是为了满足markdown语法
            created_t=created_time,
            category=cate,
            auther=user,
        )
        post.tags.add(tag1, tag2)
        post.save()

    fake = faker.Faker('zh_CN')
    for _ in range(100):  # Chinese
        tags = Tags.objects.order_by('?')
        tag1 = tags.first()
        tag2 = tags.last()
        cate = Category.objects.order_by('?').first()
        created_time = fake.date_time_between(start_date='-1y', end_date="now",
                                              tzinfo=timezone.get_current_timezone())
        post = Text.objects.create(
            title=fake.sentence().rstrip('.'),
            body='\n\n'.join(fake.paragraphs(10)),

            created_t=created_time,
            category=cate,
            auther=user,
        )
        post.tags.add(tag1, tag2)
        post.save()

    print('create some comments')
    for post in Text.objects.all()[:20]:
        post_created_time = post.created_t
        delta_in_days = '-' + str((timezone.now() - post_created_time).days) + 'd'  #要注意的是评论的发布时间必须位于被评论文章的发布时间和当前时间之间
        for _ in range(random.randrange(3, 15)):
            Comment.objects.create(
                    name=fake.name(),
                    email=fake.email(),
                    url=fake.uri(),
                    text=fake.paragraph(),
                    created_t=fake.date_time_between(
                        start_date=delta_in_days,
                        end_date="now",
                        tzinfo=timezone.get_current_timezone()),
                    post=post,
                )

    print('done!')
