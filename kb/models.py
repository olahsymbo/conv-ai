from django.db import models


class Shop(models.Model):
    """
    create a model as an ORM to access the corresponding
    data table in our postgres DB.
    """
    class Meta:
        db_table = 'shop'

    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()
    temperature = models.CharField(max_length=250)
    duration = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.id} {self.timestamp} {self.temperature} {self.duration}"
