from django.contrib import admin
from .models import ProductModel


# Register your models here.
@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
  
  list_display = ("code", "name", "created_at", "updated_at")
  