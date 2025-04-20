from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(blank=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    appeared_at = models.DateTimeField('Время появления')
    disappeared_at = models.DateTimeField('Время исчезновения')

    Level = models.IntegerField(blank=True)
    Health = models.IntegerField(blank=True)
    Attack = models.IntegerField(blank=True)
    Protection = models.IntegerField(blank=True)
    Endurance = models.IntegerField(blank=True)