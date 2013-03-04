from django.contrib.gis import admin
from directions.models import Bus, Stop


admin.site.register(Bus)

admin.site.register(Stop, admin.GeoModelAdmin)
