from collections import OrderedDict
from django.db import models

class StockPrice(models.Model):

    ric = models.CharField(null = False, max_length = 20)
    relative_date = models.IntegerField()
    date = models.DateField(null = False)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    adjusted_close = models.FloatField()
    return_value = models.FloatField()
    pc_return = models.FloatField()
    cm_return = models.FloatField()
    av_return = models.FloatField()

    class Meta:
        unique_together = (('ric', 'date'),)

    def to_dict(self):
        return OrderedDict([
            ('RelativeDate', self.relative_date),
            ('Date', self.date.strftime('%Y-%m-%d')),
            ('Return', self.return_value),
            ('Open', self.open),
            ('High', self.high),
            ('Close', self.close),
            ('Volume', self.volume),
            ('AdjustedClose', self.adjusted_close),
            ('PC_Return', self.pc_return),
            ('CM_Return', self.cm_return),
            ('AV_Return', self.av_return),
        ])
