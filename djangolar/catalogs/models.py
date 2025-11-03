from django.db import models


class Cuisines(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Restaurants(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.FloatField()
    geojson = models.JSONField()
    cuisine = models.ForeignKey(Cuisines, on_delete=models.PROTECT)


class Categories(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


class DeliveryZones(models.Model):
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    geojson = models.JSONField()
    min_delivery_price = models.DecimalField(max_digits=10, decimal_places=2)

class Dishes(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Options(models.Model):
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
