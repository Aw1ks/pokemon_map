# Generated by Django 5.2 on 2025-04-28 11:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0014_alter_pokemonentity_attack_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='image',
            field=models.ImageField(blank=True, upload_to='static\\images', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon', to='pokemon_entities.pokemon', verbose_name='Покемон'),
        ),
    ]
