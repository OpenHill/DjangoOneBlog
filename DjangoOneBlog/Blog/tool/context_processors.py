from ..models import CategoryTable, BlogSettingsTable, ArticleTable


def get_class(request):
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

    # 网站全局设置
    title = BlogSettingsTable.get_value('sitename')
    title_description = BlogSettingsTable.get_value('site_description')
    if not title:
        title = '博客名在后台设置中设置'
    if not title_description:
        title_description = '博客描述在后台设置中设置'

    setting = {
        'title': title,
        'title_description': title_description
    }

    return {
        'public_top_data': category_list,
        'public_setting': setting
    }


def views_article(request):
    ar = ArticleTable.objects.filter(status='n').order_by('-views').all()[:5]
    return {
        'views_article': ar
    }

def lately_article(request):
    ar = ArticleTable.objects.filter(status='n').order_by('-pub_time').all()[:5]
    return {
        'lately_article': ar
    }