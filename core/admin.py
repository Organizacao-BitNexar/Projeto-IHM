from django.contrib import admin
from .models import CorpoCeleste

@admin.register(CorpoCeleste)
class CorpoCelesteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria')
    search_fields = ('nome',)
    list_filter = ('categoria',)
# Register your models here.
