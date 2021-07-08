from django.db import models


class Shop(models.Model):
    """
    create a model as an ORM to access the corresponding
    data table in our postgres DB.
    """
    class Meta:
        db_table = 'shop'

    id = models.IntegerField(primary_key=True)
    product = models.CharField(max_length=250)
    brand = models.CharField(max_length=250)
    amount = models.CharField(max_length=250)
    url = models.CharField(max_length=250)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.id} {self.product} {self.url} {self.date}"
