from django.urls import path
# from django.conf.urls import handler404
from .view.index import index
from .view.article import ArticleIndexListView, ArticleSearchListView, ArticleClassListView, ArticleIndexView

# from .view.error import page_not_found

urlpatterns = [
    # Index
    path('', ArticleIndexListView.as_view(), name='index'),
    path('article/<int:id>', ArticleIndexView.as_view(), name='article'),
    path('search/<str:key>/<int:page>', ArticleSearchListView.as_view(), name='search'),
    # path('search/<int:page>', article_search, name='search'),
    path('class/<int:id>/<int:page>', ArticleClassListView.as_view(), name='class')

]
# handler404 = page_not_found
