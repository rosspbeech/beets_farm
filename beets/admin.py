from django.contrib import admin
from beets.models import Beet, Persona, UserProfile


class BeetAdmin(admin.ModelAdmin):
    list_display = ['name', 'about', 'persona']


class PersonaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Persona, PersonaAdmin)
admin.site.register(Beet, BeetAdmin)
admin.site.register(UserProfile)