from django.db import models
from django.utils import timezone


class Pokemon(models.Model):
    """Информация о покемоне."""

    title = models.CharField('Название (рус.)', max_length=200)
    title_en = models.CharField('Название (англ.)', max_length=200)
    title_jp = models.CharField('Название (яп.)', max_length=200)
    image = models.ImageField('Изображение')
    description = models.TextField('Описание', default='Описание в разработке')

    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='previous_evolutions',
        verbose_name='Предыдущая эволюция'
    )    

    def __str__(self):
        return f'{self.title}'

class PokemonEntity(models.Model):
    """Информация о местоположении покемона."""

    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')

    appeared_at = models.DateTimeField('Время появления', default=timezone.now)
    disappeared_at = models.DateTimeField('Время появления', default=timezone.now)

    level = models.IntegerField('Уровень', blank=True, null=True)   
    health = models.IntegerField('Здоровье', blank=True, null=True)  
    attack = models.IntegerField('Атака', blank=True, null=True)  
    protection = models.IntegerField('Защита', blank=True, null=True) 
    stamina = models.IntegerField('Выносливость', blank=True, null=True)
