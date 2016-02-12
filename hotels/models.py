from django.db import models
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from hh.models import CommonInfo


class Tariff(CommonInfo):
    """
    Hotel tariffs
    """
    def validate_is_default(is_default):
        if not is_default and not Tariff.objects.filter(is_default=True).count():
            raise ValidationError('One of the tariffs should be the default')

    name = models.CharField(max_length=80)
    is_default = models.BooleanField(default=False, verbose_name='Is default?', validators=[validate_is_default])
    minimal_commission = models.PositiveIntegerField()

    def delete(self, *args, **kwargs):
        if self.is_default:
            raise Exception('Cannot delete default tariff')
        super(Tariff, self).delete(*args, **kwargs)


class TariffElement(models.Model):
    """
    Tariff element
    """
    PERCENT_VALIDATORS = [MaxValueValidator(100)]

    start_sum = models.PositiveIntegerField()
    end_sum = models.PositiveIntegerField()
    commission = models.PositiveIntegerField(validators=PERCENT_VALIDATORS)
    agent_commission = models.PositiveIntegerField(validators=PERCENT_VALIDATORS)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)

    def clean(self):
        if self.start_sum >= self.end_sum:
            raise ValidationError('Start sum cannot exceed end sum')

