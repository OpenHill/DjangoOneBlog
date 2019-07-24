# Generated by Django 2.2.3 on 2019-07-22 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0004_auto_20190721_1314'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articletable',
            options={'get_latest_by': 'id', 'ordering': ['-article_order', '-pub_time'], 'verbose_name': '文章管理', 'verbose_name_plural': '文章管理'},
        ),
        migrations.AlterModelOptions(
            name='categorytable',
            options={'verbose_name': '分类管理', 'verbose_name_plural': '分类管理'},
        ),
        migrations.AlterModelOptions(
            name='commenttable',
            options={'verbose_name': '评论管理', 'verbose_name_plural': '评论管理'},
        ),
        migrations.AlterModelOptions(
            name='tagtable',
            options={'ordering': ['name'], 'verbose_name': '标签管理', 'verbose_name_plural': '标签管理'},
        ),
    ]
