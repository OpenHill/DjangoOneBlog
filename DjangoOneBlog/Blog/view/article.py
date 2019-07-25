from django.shortcuts import render, redirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView

from ..models import ArticleTable, BlogSettingsTable, CommentTable, CategoryTable
from django.db.models import Q
from ..forms import SearchForm
from ..tool.ArticleTool import HandleArticle
import markdown


# mixin
class TopMixin:
    category_object_list = CategoryTable.objects.all()

    category_model = {"id": None, "name": None, "childes": []}

    def get_class(self):
        category_list = []

        def parse(obj):
            id = obj.id
            name = obj.name
            self_model = {"id": id, "name": name, "childes": []}
            if obj.parent_category:
                # 有父亲级
                childes = CategoryTable.objects.filter(parent_category=obj).all()
                if childes:
                    for i in childes:
                        self_model['childes'].append(parse(i))
                return self_model
            else:
                for i in CategoryTable.objects.filter(parent_category=obj).all():
                    self_model["childes"].append(parse(i))

                return self_model

        for i in CategoryTable.objects.filter(parent_category=None).all():
            category_list.append(parse(i))
        return category_list


class ArticleIndexView(TopMixin, DetailView):
    model = ArticleTable
    template_name = 'article.html'
    context_object_name = 'article'
    pk_url_kwarg = 'id'

    @method_decorator(cache_page(10))
    def get(self, request, *args, **kwargs):
        """
        重构GET,添加缓存
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = super().get(request, *args, **kwargs)

        return response

    def get_queryset(self):
        id = self.kwargs.get('id')
        return self.model.objects.filter(status='n', id=id).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'].body = HandleArticle.handleBody(context['article'].body, True)

        articleObj = self.get_queryset()
        nextArticleObj = articleObj.next_article
        previousArticleObj = articleObj.prev_article

        paginator = self.get_paginator(nextArticleObj, previousArticleObj)

        context['top'] = self.get_class()
        context['paginator'] = paginator
        context['comment'] = self.get_comment(articleObj)

        return context

    def get_paginator(self, next_obj, perv_obj):
        """
        获取文章的下一篇与下另一篇
        :param next_obj:
        :param perv_obj:
        :return:
        """
        paginator = {
            "ifNext": True if next_obj else False,
            "nextPage": [next_obj.__str__(), next_obj.id] if next_obj else None,
            "ifPrevious": True if perv_obj else False,
            "previousPage": [perv_obj.__str__(), perv_obj.id] if perv_obj else None,
        }

        return paginator

    def get_comment(self, articleObj):
        """
        获取文章下的评论
        :param articleObj:
        :return:
        """
        comment = {
            "status": articleObj.comment_status == 'o' and BlogSettingsTable.objects.get(id=1).open_site_comment,
            "commentlist": CommentTable.objects.filter(article=articleObj).all()
        }
        return comment

    # 首页


class ArticleIndexListView(TopMixin, ListView):
    model = ArticleTable
    template_name = "index.html"
    context_object_name = "article_list"
    pageCount = BlogSettingsTable.get_value("article_count") or 10

    @method_decorator(cache_page(10))
    def get(self, request, *args, **kwargs):
        """重构GET,添加缓存
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        article_all = []
        article = ArticleTable.objects.filter(status='n').all()
        for i in article:
            i.body = HandleArticle.handleBody(i.body, False)
            article_all.append(i)
        return article_all

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 自定义分页
        article_num = len(self.get_queryset())
        page = int(self.request.GET.get('page', None) or 1)

        context['diy_paginator'] = HandleArticle.handlePaginator_page(article_num, page, self.pageCount, "/?page={}")
        context['top'] = self.get_class()
        return context


class ArticleSearchListView(TopMixin, ListView):
    model = ArticleTable
    template_name = "index.html"
    context_object_name = "article_list"
    pageCount = BlogSettingsTable.get_value("article_count") or 10

    @method_decorator(cache_page(10))
    def get(self, request, *args, **kwargs):
        """重构GET,添加缓存
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        key = self.kwargs.get("key")
        # page = self.kwargs.get("page")

        article_all = []
        article = ArticleTable.objects.filter(
            Q(title__contains=key) | Q(body__contains=key), status='n').all()
        for i in article:
            i.body = HandleArticle.handleBody(i.body, False)
            article_all.append(i)
        return article_all

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 自定义分页
        article_num = len(self.get_queryset())
        page = int(self.kwargs.get('page', None) or 1)
        key = self.kwargs.get('key', " ")

        context['top'] = self.get_class()
        context['diy_paginator'] = HandleArticle.handlePaginator_id_page(
            allNum=article_num, id=key, page=page, pageCount=self.pageCount,
            formatstr="/search/{}/{}")

        return context


class ArticleClassListView(TopMixin, ListView):
    model = ArticleTable
    template_name = "index.html"
    context_object_name = "article_list"
    pageCount = BlogSettingsTable.get_value("article_count") or 10

    @method_decorator(cache_page(10))
    def get(self, request, *args, **kwargs):
        """重构GET,添加缓存
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        id = self.kwargs.get("id")
        category = CategoryTable.objects.get(pk=id)
        parent_category = category.parent_category

        article_all = []

        if not parent_category:
            # 不存在父级
            all_children = category.get_category_children()
            all_article = []
            if all_children:
                for i in all_children:
                    article_low_list = ArticleTable.objects.filter(categorys=i).all()
                    if article_low_list:
                        for j in article_low_list:
                            j.body = HandleArticle.handleBody(j.body, False)
                            all_article.append(j)

            article_all = list(set(all_article))

        return article_all

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 自定义分页
        article_num = len(self.get_queryset())
        page = int(self.kwargs.get('page', None) or 1)
        id = int(self.kwargs.get('id'))

        context['top'] = self.get_class()
        context['diy_paginator'] = HandleArticle.handlePaginator_id_page(
            allNum=article_num, id=id, page=page, pageCount=self.pageCount,
            formatstr="/class/{}/{}")

        return context
