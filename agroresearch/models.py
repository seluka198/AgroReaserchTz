from django.db import models
from django.contrib.gis.db import models 
from django.contrib.auth.models import User


class AgriculturalArea(models.Model):
    name = models.CharField(max_length=255)
    geom = models.PolygonField() 

    def __str__(self):
        return self.name
class RainfallScheme(models.Model):
    scheme_name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    rainfall_mm = models.FloatField()
    year = models.IntegerField()
    location = models.PointField()

    def __str__(self):
        return self.scheme_name

from django.contrib.gis.db import models

class RainfallData(models.Model):
    region = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    jan = models.FloatField()
    feb = models.FloatField()
    mar = models.FloatField()
    # ... hadi dec
    dec = models.FloatField()
    geom = models.PointField(srid=4326)

    def __str__(self):
        return f"{self.region} ({self.latitude}, {self.longitude})"

from django.db import models

class Forecast(models.Model):
    date = models.DateField()
    predicted_rainfall = models.FloatField()

    def __str__(self):
        return f"{self.date.strftime('%B %Y')}: {self.predicted_rainfall:.2f} mm"
def forecast_view(request):
    return render(request, 'forecast.html')