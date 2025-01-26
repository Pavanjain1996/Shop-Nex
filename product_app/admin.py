from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.Rating)
admin.site.register(models.Cart)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
