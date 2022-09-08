from multiprocessing import context
import profile
from urllib import request
from xml.etree.ElementTree import Comment
from accounts.models import Profile
from api.v1.accounts.serializers import MinimalSerializer
from posts.models import PostComments, PostLikes, Posts
from rest_framework import serializers

class PostSerializer(serializers.Serializer):
    post = serializers.FileField()
    description = serializers.CharField() 

class PostViewSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    class Meta:
        model = Posts
        fieilds = (
            'id',
            'post',
            'description',
            'profile',
            'likes_count',
            'liked',
            'comment_count',
        )
        exclude = ('auto_id','creator','updater','user',)

    def get_profile(self,instance):
        request = self.context.get('request')
        instance = instance.user
        serialize = MinimalSerializer(
            instance,
            context = {
                "request":request
            }
        ).data
        profile = serialize
        return profile
    
    def get_likes_count(self,instance):
        like = PostLikes.objects.filter(post = instance).count()
        likes_count = like

        return likes_count

    def get_liked(self,instance):
        request = self.context.get('request')
        profile = Profile.objects.get(user = request.user)
        if PostLikes.objects.filter(post = instance,liked_user = profile).exists():
            liked = 'true'
        else:
            liked = 'false'
        return liked
    
    def get_comment_count(self,instance):
        comment_count = PostComments.objects.filter(post = instance).count()
        return comment_count

class CommentsViewSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    class Meta:
        model = PostComments
        fields = (
            'id',
            'auto_id',
            'comment',
            'profile',
        )

    def get_profile(self,instance):
        data = instance.commented_user
        serialized = MinimalSerializer(
            data,
            context = {
                "requext":request,
            }
        ).data
        profile = serialized
        return profile
class PostCommentSerializer(serializers.Serializer):
    comment = serializers.CharField()
    