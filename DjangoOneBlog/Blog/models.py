from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from mdeditor.fields import MDTextField
import copy


# 字段采用全小写
# Create your models here.

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)


class ArticleTable(BaseModel):
    ARTICLE_STATUS = (
        ("c", '删除'),
        ("d", "草稿"),
        ("n", '正常')
    )
    COMMENT_STATUS = (
        ("c", "关闭"),
        ("o", "开启")
    )
    TYPE = (
        ("t", "技术"),
        ("g", "闲聊")
    )

    title = models.CharField('标题', max_length=200, unique=True)
    body = MDTextField('正文')
    pub_time = models.DateTimeField('发布时间', blank=False, null=False, default=now)
    status = models.CharField('文章状态', max_length=1, choices=ARTICLE_STATUS, default='n')
    comment_status = models.CharField('评论状态', max_length=1, choices=COMMENT_STATUS, default='o')
    type = models.CharField('类型', max_length=1, choices=TYPE, default='g')
    views = models.PositiveIntegerField('浏览量', default=0)
    author = models.CharField('作者', default=settings.AUTHOR_NAME, max_length=50)
    article_order = models.IntegerField('排序,数字越大越靠前', blank=False, null=False, default=0)
    categorys = models.ForeignKey('CategoryTable', verbose_name='分类', on_delete=models.CASCADE, blank=False, null=False)
    tags = models.ManyToManyField('TagTable', verbose_name='标签集合', blank=True)

    def __str__(self):
        return self.title

    def get_body(self):
        return self.body

    def next_article(self):
        # 下一篇
        return ArticleTable.objects.filter(id__gt=self.id, status=2).order_by('id').first()

    def prev_article(self):
        # 前一篇
        return ArticleTable.objects.filter(id__lt=self.id, status=2).first()

    # 元类
    # http://www.liujiangblog.com/course/django/99
    class Meta:
        get_latest_by = 'id'
        ordering = ['-article_order', '-pub_time']
        verbose_name = '文章管理'
        verbose_name_plural = verbose_name


class CategoryTable(BaseModel):
    name = models.CharField('分类名', max_length=30, unique=True)
    parent_category = models.ForeignKey('self', verbose_name="父级分类", blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    def __str__(self):
        return self.name

    def get_category_parent(self):
        """
        递归获得当前目录的父级分类，用于面包屑导航
        :return:
        """
        category_list = []

        def parse(category):
            category_list.append(self)
            if category.parent_category:
                parse(category)

        parse(self)
        return category_list

    def get_category_children(self):
        """
        获得当前目录的子级
        :return:
        """

        categorys = []
        all_categorys = CategoryTable.objects.all()

        def parse(category):
            if category not in categorys:
                categorys.append(category)
            childs = all_categorys.filter(parent_category=category)
            for child in childs:
                if category not in categorys:
                    categorys.append(child)
                parse(child)

        parse(self)
        print(len(categorys), len(all_categorys))
        return categorys

    class Meta:
        verbose_name = '分类管理'
        verbose_name_plural = verbose_name


class TagTable(BaseModel):
    """文章标签"""
    name = models.CharField('标签名', max_length=30, unique=True)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'tag_name': self.slug})

    def get_article_count(self):
        return ArticleTable.objects.filter(tags__name=self.name).distinct().count()

    class Meta:
        ordering = ['name']
        verbose_name = "标签管理"
        verbose_name_plural = verbose_name


class CommentTable(models.Model):
    content = models.CharField("评论内容", max_length=200)  # 200长
    article = models.ForeignKey('ArticleTable', verbose_name="评论的文章", blank=True, on_delete=models.CASCADE, )

    def __str__(self):
        return self.article.title + " --评论--> " + self.content

    class Meta:
        verbose_name = '评论管理'
        verbose_name_plural = verbose_name


class BlogSettingsTable(models.Model):
    '''站点设置 '''
    sitename = models.CharField("网站名称", max_length=200, null=False, blank=False, default='')
    site_description = models.TextField("网站描述", max_length=1000, null=False, blank=False, default='')
    site_seo_description = models.TextField("网站SEO描述", max_length=1000, null=False, blank=False, default='')
    site_keywords = models.TextField("网站关键字", max_length=1000, null=False, blank=False, default='')
    article_sub_split_str = models.CharField("文章摘要分隔符", default=300, max_length=20, null=False, blank=False)
    sidebar_article_count = models.IntegerField("侧边栏文章数目", default=10)
    article_count = models.IntegerField("分页文章数目", default=10)
    sidebar_comment_count = models.IntegerField("侧边栏评论数目", default=5)
    open_site_comment = models.BooleanField('是否打开网站评论功能', default=True)
    beiancode = models.CharField('备案号', max_length=2000, null=True, blank=True, default='123456')
    analyticscode = models.TextField("网站统计代码", max_length=1000, null=False, blank=False, default='')
    show_gongan_code = models.BooleanField('是否显示公安备案号', default=False, null=False)
    gongan_beiancode = models.TextField('公安备案号', max_length=2000, null=True, blank=True, default='123456')
    resource_path = models.CharField("静态文件保存地址", max_length=300, null=False, default='/var/www/resource/')

    class Meta:
        verbose_name = '网站配置'
        verbose_name_plural = verbose_name

    @staticmethod
    def get_value(key):
        setting = BlogSettingsTable.objects.filter(id=1).first()
        if setting:
            if hasattr(setting, key):
                return getattr(setting, key)
        return None

    def __str__(self):
        return self.sitename

    def clean(self):
        if BlogSettingsTable.objects.exclude(id=self.id).count():
            raise ValidationError(_('只能有一个配置'))
