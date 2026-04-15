from django.db import models


class Animal(models.Model):
    scientific_name = models.CharField(verbose_name='Scientific name', max_length=150)
    common_name = models.CharField(verbose_name='Common name', max_length=250)
    group = models.CharField(verbose_name='Spicies group', max_length=100)
    conservation_status = models.CharField(verbose_name='Conservation', max_length=10)
    image = models.URLField(verbose_name='image URL', max_length=200)

    def __str__(self):
        return self.common_name