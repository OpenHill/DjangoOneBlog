import markdown
from ..models import BlogSettingsTable


class HandleArticle:

    @staticmethod
    def handleBody(body: str, is_more: bool):
        """
        处理文章内容
        :param body: 全部文章内容
        :param is_more: 是否是全部 yes is True
        :return: str
        """
        splitstr = BlogSettingsTable.objects.get(pk=1).article_sub_split_str
        if is_more:
            body = body.replace(splitstr, "")

        else:
            body = body.split(splitstr)[0]

        handlebody = markdown.markdown(body, extensions=['markdown.extensions.extra',
                                                         'markdown.extensions.tables',
                                                         'markdown.extensions.codehilite',
                                                         'markdown.extensions.toc'])
        return handlebody

    @staticmethod
    def handlePaginator_id_page(allNum: int, id: int, page: int, pageNum: int, formatstr: str):
        """
        处理 /xxx/id/page  等通用分类的 Func
        :param allNum: 所有数量
        :param id: id
        :param page: 当前页
        :param pageNum: 分页文章数量
        :param formatstr: 格式字符串
        :return: {"ifNext": False,"nextPageNum": None,"ifPrevious": False,"previousNum": None}
        """

        # 分页Model
        paginator = {
            "ifNext": False,
            "nextPageNum": None,
            "ifPrevious": False,
            "previousNum": None
        }

        # 是否有下一页
        if allNum > page * pageNum:
            paginator["ifNext"] = True
            paginator["nextPageNum"] = formatstr.format(id, page + 1)

        # 是否有上一页
        if page > 1 and allNum >= page * pageNum:
            paginator["ifPrevious"] = True
            paginator["previousNum"] = formatstr.format(id, page - 1)

        return paginator
