from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _


class PoI(models.Model):
    name = models.CharField(_('name'), max_length=255)
    external_id = models.BigIntegerField(_('external id'))
    lon = models.FloatField(_('longitude'))
    lat = models.FloatField(_('latitude'))
    category = models.CharField(_('category'), max_length=150)
    ratings = ArrayField(models.DecimalField(max_digits=12, decimal_places=2))

    class Meta:
        verbose_name = _('point of interest')
        verbose_name_plural = _('point of interests')

    @property
    def avg_rating(self):
        return sum(self.ratings) / len(self.ratings)
