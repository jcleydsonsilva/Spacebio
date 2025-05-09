# Generated by Django 5.0.1 on 2024-08-27 14:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0003_article_author_affiliation_details"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="doi",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="journal_issn",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="journal_issue",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="journal_volume",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="journal_year_of_publication",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="language",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="pmcid",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="pmid",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="pub_model",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="publication_status",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="source",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
