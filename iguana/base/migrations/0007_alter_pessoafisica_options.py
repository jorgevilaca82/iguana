# Generated by Django 3.2 on 2021-05-11 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0006_auto_20210504_1746"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="pessoafisica",
            options={"ordering": ["-pk"]},
        ),
    ]
