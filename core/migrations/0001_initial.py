# Generated by Django 4.2.3 on 2023-07-20 18:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True)),
                ('file_format', models.CharField(choices=[('pdf', 'PDF'), ('txt', 'TXT'), ('docx', 'DOCX'), ('doc', 'DOC'), ('xml', 'XML'), ('json', 'JSON')], default='pdf', max_length=4)),
                ('file', models.FileField(max_length=5242880, upload_to='docs', validators=[django.core.validators.FileExtensionValidator(['pdf', 'txt', 'docx', 'doc', 'xml', 'json'])])),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('shared_users', models.ManyToManyField(blank=True, related_name='shared_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
