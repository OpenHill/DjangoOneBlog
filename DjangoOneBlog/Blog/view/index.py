# from django.core.paginator import Paginator
from django.shortcuts import render
from ..models import ArticleTable
import markdown


def index(request, page=1):
    # 单页几个内容
    pageNum = 10
    # 非负
    page = abs(page)

    # 所有合格数据
    article_list_all = ArticleTable.objects.filter(status='n').all()

    # 切割数据
    article_list = article_list_all[(page - 1) * pageNum:page * pageNum]

    # 分页Model
    paginator = {
        "ifNext": False,
        "nextPageNum": None,
        "ifPrevious": False,
        "previousNum": None
    }

    # 是否有下一页
    if len(article_list_all) > page * pageNum:
        paginator["ifNext"] = True
        paginator["nextPageNum"] = page + 1

    # 是否有上一页
    if page > 1 and len(article_list_all) > page * pageNum:
        paginator["ifPrevious"] = True
        paginator["previousNum"] = page - 1

    # 数据处理
    for i, item in enumerate(article_list):
        article_list[i].body = article_list[i].body.split("(====)")[0]
        article_list[i].body = markdown.markdown(article_list[i].body,
                                                 extensions=['markdown.extensions.extra',
                                                             'markdown.extensions.tables',
                                                             'markdown.extensions.codehilite',
                                                             'markdown.extensions.toc', ])
    return render(request, 'index.html', {"article_list": article_list, "paginator": paginator})



