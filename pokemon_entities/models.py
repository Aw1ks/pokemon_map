from django.db import models  # noqa F401
from django.utils import timezone


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(blank=True)
    description = models.TextField(default='Описание в разработке')

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    appeared_at = models.DateTimeField(default=timezone.now)
    disappeared_at = models.DateTimeField(default=timezone.now)

    level = models.IntegerField(blank=True, null=True)   
    health = models.IntegerField(blank=True, null=True)  
    attack = models.IntegerField(blank=True, null=True)  
    protection = models.IntegerField(blank=True, null=True) 
    stamina = models.IntegerField(blank=True, null=True)