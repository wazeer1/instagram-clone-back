from django.contrib import admin

from accounts.models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'date_added', 'name', 'phone', 'email',
                     'is_verified', 'password', 'gender', 'dob')
    ordering = ('-date_added',)
    search_fields = ('phone', 'pk', 'user__username', 'name')
    
admin.site.register(Profile,ProfileAdmin)