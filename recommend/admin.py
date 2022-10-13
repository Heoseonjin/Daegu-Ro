from django.contrib import admin
from .models import Recommend, Category

# Register your models here.
admin.site.register(Recommend)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategoryAdmin)