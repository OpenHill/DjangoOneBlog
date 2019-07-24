# Generated by Django 2.2.3 on 2019-07-21 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_commenttable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commenttable',
            name='article',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Blog.ArticleTable', verbose_name='评论的文章'),
        ),
    ]
