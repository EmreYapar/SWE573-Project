# Generated by Django 2.0.2 on 2019-06-09 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_remove_wikidata_associated_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoursePart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('associated_course_id', models.IntegerField()),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('body', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('associated_coursepart_id', models.IntegerField()),
                ('question', models.CharField(max_length=255)),
                ('trueAnswer', models.CharField(max_length=255)),
                ('falseAnswer1', models.CharField(max_length=255)),
                ('falseAnswer2', models.CharField(max_length=255)),
                ('falseAnswer3', models.CharField(max_length=255)),
            ],
        ),
    ]
