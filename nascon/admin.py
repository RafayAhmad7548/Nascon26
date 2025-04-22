from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Accommodation)
admin.site.register(models.Event)
# admin.site.register(Eventround)
# admin.site.register(Participantevent)
admin.site.register(models.Payment)
admin.site.register(models.Society)
# admin.site.register(Sponsor)  
admin.site.register(models.Sponsorshippackage)
admin.site.register(models.Team)
admin.site.register(models.User)
admin.site.register(models.Venue)