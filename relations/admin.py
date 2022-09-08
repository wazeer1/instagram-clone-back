from django.contrib import admin

from relations.models import Followers

# Register your models here.
# class FollowersAdmin(admin.ModelAdmin):
#     list_display = ('id',)
#     ordering = ('date_added',)
# admin.site.register(Followers,FollowersAdmin)
admin.site.register(Followers)