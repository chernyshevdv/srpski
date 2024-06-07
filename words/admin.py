from django.contrib import admin
import words.models as models


class WordInline(admin.TabularInline):
    model = models.Word


class WordListAdmin(admin.ModelAdmin):
    model = models.WordList
    inlines = [WordInline]


admin.site.register(models.WordList, WordListAdmin)