from django.contrib import admin

from .models import PoI


@admin.register(PoI)
class PoIAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'external_id', 'category', 'avg_rating')
    list_filter = ('category',)
    search_fields = ('id', 'internal_id')
