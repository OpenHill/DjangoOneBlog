from django.urls import path
# from django.conf.urls import handler404
from .view.index import index
from .view.article import article, article_search, article_class, ArticleIndexListView

# from .view.error import page_not_found

urlpatterns = [
    # Index
    path('', ArticleIndexListView.as_view(), name='index'),
    # path('popop/<int:id>', ArticleIndexListView.as_view(), name='indexs'),
    # path('<int:page>', ArticleIndexListView.as_view(), name='indexPage'),
    path('article/<int:id>', article, name='article'),
    path('search/<str:key>/<int:page>', article_search, name='search'),
    # path('search/<int:page>', article_search, name='search'),
    path('class/<int:id>/<int:page>', article_class, name='class')

]
# handler404 = page_not_found
