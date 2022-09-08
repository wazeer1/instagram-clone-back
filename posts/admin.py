from django.contrib import admin
from posts.models import PostComments, Status
from posts.models import PostLikes

from posts.models import Posts

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','description')
    ordering = ('-date_added',)
admin.site.register(Posts,PostAdmin)

class LikesAdmin(admin.ModelAdmin):
    list_display = ('id',)
    ordering=('date_added',)
admin.site.register(PostLikes,LikesAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','comment')
    ordering=('date_added',)
admin.site.register(PostComments,CommentAdmin)


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id',)
admin.site.register(Status,StatusAdmin)