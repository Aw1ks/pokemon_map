from django.db import models
from django.utils import timezone


class Pokemon(models.Model):
    """Информация о покемоне."""

    title = models.CharField('Название (рус.)', max_length=200, default='Название в разработке', blank=True)
    title_en = models.CharField('Название (англ.)', max_length=200, default='Название в разработке', blank=True)
    title_jp = models.CharField('Название (яп.)', max_length=200, default='Название в разработке', blank=True)
    image = models.ImageField(
        'Изображение',
        upload_to='static\images',
        blank=True
    )
    description = models.TextField('Описание', default='Описание в разработке', blank=True)

    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name='Предыдущая эволюция'
    )

    def __str__(self):
        return f'{self.title}'

class PokemonEntity(models.Model):
    """Информация о местоположении покемона."""

    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE, 
        verbose_name='Тип покемона',
        related_name='entities'
    )

    appeared_at = models.DateTimeField('Время появления', default=timezone.now, null=True)
    disappeared_at = models.DateTimeField('Время появления', default=timezone.now, null=True)

    level = models.PositiveIntegerField('Уровень', blank=True, null=True)   
    health = models.PositiveIntegerField('Здоровье', blank=True, null=True)  
    attack = models.PositiveIntegerField('Атака', blank=True, null=True)  
    protection = models.PositiveIntegerField('Защита', blank=True, null=True) 
    stamina = models.PositiveIntegerField('Выносливость', blank=True, null=True)
