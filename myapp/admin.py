from django.contrib import admin
from .models import offer,arrivals , StoreItem,Cart


class offerAdmin(admin.ModelAdmin):
    list_display = ('name','description')
    list_filter = ('isactive','startdate','enddate')

admin.site.register(offer,offerAdmin)

admin.site.register(arrivals)

admin.site.register(StoreItem)

admin.site.register(Cart)

