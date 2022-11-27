from django.contrib import admin
from .models import usage, Category
# Register your models here.


class usageAdmin(admin.ModelAdmin):
    list_display = ('power', 'hybrid', 'owner', 'category', 'date',)
    search_fields = ('hybrid', 'category', 'date',)

    list_per_page = 5


admin.site.register(usage, )
admin.site.register(Category)
