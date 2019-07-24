from django.contrib import admin
from .models import ArticleTable, BlogSettingsTable, CategoryTable, CommentTable, TagTable

# Register your models here.

admin.site.register(ArticleTable)
admin.site.register(BlogSettingsTable)
admin.site.register(CategoryTable)
admin.site.register(CommentTable)
admin.site.register(TagTable)
