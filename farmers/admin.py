from django.contrib import admin

from farmers.models import Farmer


# Register your models here.
class FarmerAdmin(admin.ModelAdmin):
    list_display = ("phone_number","first_name")







# admin.site.register(User, UserAdmin)
admin.site.register(Farmer, FarmerAdmin)