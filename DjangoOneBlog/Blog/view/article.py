from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.views.generic import ListView

from ..models import ArticleTable, BlogSettingsTable, CommentTable, CategoryTable
from django.db.models import Q
from ..forms import SearchForm
from ..tool.ArticleTool import HandleArticle
import markdown


def article(request, id):
    # 绝对值
    id = abs(id)

    # 元数据
    articleObj = ArticleTable.objects.filter(id=id).first()

    # 是否成功
    if not articleObj:
        return redirect(request.path)

    # 下一页 & 上一页
    nextArticleObj = ArticleTable.objects.filter(id=id + 1).first()
    previousArticleObj = ArticleTable.objects.filter(id=id - 1).first()

    # 浏览量+1
    articleObj.views = articleObj.views + 1
    articleObj.save()

    # 处理数据
    articleObj.body = HandleArticle.handleBody(articleObj.body, True)

    # 分页模型
    paginator = {
        "ifNext": True if nextArticleObj else False,
        "nextPage": [nextArticleObj.__str__(), nextArticleObj.id] if nextArticleObj else None,
        "ifPrevious": True if previousArticleObj else False,
        "previousPage": [previousArticleObj.__str__(), previousArticleObj.id] if previousArticleObj else None,
    }

    # 评论模型
    comment = {
        "status": articleObj.comment_status == 'o' and BlogSettingsTable.objects.get(id=1).open_site_comment,
        "commentlist": CommentTable.objects.filter(article=articleObj).all()
    }

    return render(request, 'article.html', {"article": articleObj,
                                            "paginator": paginator,
                                            "comment": comment})


def article_search(request, key, page):
    # 保证正确性
    page = int(page)
    page = abs(page)

    # 从设置表里拉取数据
    pageNum = 10
    settings = BlogSettingsTable.objects.get(pk=1)
    if settings:
        pageNum = settings.article_count

    # 获取元数据
    article_list_all = ArticleTable.objects.filter(
        Q(title__contains=key) | Q(body__contains=key), status='n').all()

    # 切割数据
    article_list = article_list_all[(page - 1) * pageNum:page * pageNum]

    paginator = HandleArticle.handlePaginator_id_page(allNum=len(article_list_all), id=key, page=page, pageNum=pageNum,
                                                      formatstr='/search/{}/{}')

    # 数据处理
    for i, item in enumerate(article_list):
        article_list[i].body = HandleArticle.handleBody(article_list[i].body, False)

    return render(request, 'index.html', {"article_list": article_list, "paginator": paginator})


def article_class(request, id, page):
    # 初始化变量
    id = abs(id)
    page = int(page)
    page = abs(page)
    pageNum = 10

    # 从设置表里拉取数据
    settings = BlogSettingsTable.objects.get(pk=1)
    if settings:
        pageNum = settings.article_count

    # 查出元数据
    category = CategoryTable.objects.get(pk=id)

    # 判断是否存在父级
    parent_category = category.parent_category
    # if not parent_category:
    article_list_all = ArticleTable.objects.filter(categorys=category).all()
    if not parent_category:
        # 不存在父级
        all_children = category.get_category_children()
        all_article = []
        if all_children:
            for i in all_children:
                article_low_list = ArticleTable.objects.filter(categorys=i).all()
                if article_low_list:
                    for j in article_low_list:
                        all_article.append(j)

        article_list_all = list(set(all_article))

        # 切割数据
    article_list = article_list_all[(page - 1) * pageNum:page * pageNum]

    paginator = HandleArticle.handlePaginator_id_page(allNum=len(article_list_all), id=id, page=page, pageNum=pageNum,
                                                      formatstr='/class/{}/{}')

    # 数据处理
    for i, item in enumerate(article_list):
        article_list[i].body = HandleArticle.handleBody(article_list[i].body, False)

    return render(request, 'index.html', {"article_list": article_list, "paginator": paginator})


class ArticleIndexListView(ListView):
    model = ArticleTable
    template_name = "index.html"
    paginate_by = BlogSettingsTable.get_value("article_count")
    context_object_name = "article_list"
    page_kwarg = 'page'

    def get_queryset(self):
        article_all = []
        article = ArticleTable.objects.filter(status='n').all()
        for i in article:
            i.body = HandleArticle.handleBody(i.body, False)
            article_all.append(i)
        return article_all

    def get_context_data(self, **kwargs):
        context = super(ArticleIndexListView, self).get_context_data(**kwargs)
        return context

# def get_context_data(self, *, object_list=None, **kwargs):
