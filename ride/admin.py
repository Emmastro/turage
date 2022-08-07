from django.contrib import admin
from .models import *
# Register your models here.

from django.contrib.auth.admin import UserAdmin


admin.site.register(TurageUser, UserAdmin)
admin.site.register(Passenger, UserAdmin)
admin.site.register(Driver, UserAdmin)

admin.site.register(Car)
admin.site.register(Waypoint)
admin.site.register(RidingRequest)