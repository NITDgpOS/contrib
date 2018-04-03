from django.contrib import admin

from core.models import UserProfile, Repository


admin.site.register(UserProfile)
admin.site.register(Repository)
