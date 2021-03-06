# Generated by Django 3.1.1 on 2020-09-30 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('url', models.CharField(max_length=500)),
                ('comments', models.IntegerField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('removed', models.BooleanField(default=False)),
                ('content', models.CharField(max_length=4000)),
                ('subject', models.CharField(max_length=500)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commentCollector.article')),
            ],
            options={
                'unique_together': {('id',)},
            },
        ),
        migrations.CreateModel(
            name='SavedComment',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('article', models.CharField(max_length=1000)),
                ('removed', models.BooleanField(default=False)),
                ('content', models.CharField(max_length=4000)),
                ('subject', models.CharField(max_length=500)),
            ],
            options={
                'unique_together': {('id',)},
            },
        ),
        migrations.CreateModel(
            name='CommentReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=4000)),
                ('subject', models.CharField(max_length=500)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commentCollector.comment')),
            ],
            options={
                'unique_together': {('comment', 'content', 'subject')},
            },
        ),
    ]
