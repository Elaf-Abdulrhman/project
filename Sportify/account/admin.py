from django.contrib import admin

# Register your models here.
from .models import City,Sport,Athlete,Club

admin.site.register(City)
admin.site.register(Sport)
admin.site.register(Athlete)
admin.site.register(Club)