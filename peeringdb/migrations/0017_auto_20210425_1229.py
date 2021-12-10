# Generated by Django 3.2 on 2021-04-25 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("peeringdb", "0016_auto_20210420_2144")]

    operations = [
        migrations.AddField(
            model_name="facility",
            name="aka",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Also Known As"
            ),
        ),
        migrations.AddField(
            model_name="facility",
            name="name_long",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="internetexchange",
            name="aka",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Also Known As"
            ),
        ),
        migrations.AddField(
            model_name="network",
            name="name_long",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="organization",
            name="aka",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Also Known As"
            ),
        ),
        migrations.AddField(
            model_name="organization",
            name="name_long",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="internetexchange",
            name="name_long",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
