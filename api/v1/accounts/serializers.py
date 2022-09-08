from dataclasses import field
from datetime import datetime
from multiprocessing import context
from pyexpat import model
from urllib import request
from accounts.models import Profile
from relations.models import Followers
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField()
    fullname = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

class BirthDaySerializer(serializers.Serializer):
    dob = serializers.DateField()



class MinimalSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = (
            'id',
            'name', 
            'phone',
            'email',
            'photo',
            'username',
            'dob',          
        )


class FollowRequestSerializer(serializers.ModelSerializer):
    request_user = serializers.SerializerMethodField()
    class Meta:
        model = Followers
        fields = (
            'id',
            'request_user',
        )

    def get_request_user(self,instance):
        if Profile.objects.filter(pk = instance.user).exists():
            instance = Profile.objects.get(pk = instance.user)
            serialized = MinimalSerializer(
                instance,
                context={
                    "request":request
                }
            ).data
            request_user = serialized
            
        return request_user


class FollowRequestListSerializer(serializers.ModelSerializer):
    request_user = serializers.SerializerMethodField()
    class Meta:
        model = Followers
        fields = (
            'id',
            'request_user',
        )

    def get_request_user(self,instance):
        print(instance,self,'instance')
        if Profile.objects.filter(user = instance.followed_user.user).exists():
            instance = Profile.objects.get(user = instance.followed_user.user)
            serialized = MinimalSerializer(
                instance,
                context={
                    "request":request
                }
            ).data
            request_user = serialized
            
            return request_user


class UserListSerializer(serializers.ModelSerializer):
    followed = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = (
            'id',
            'name', 
            'phone',
            'email',
            'photo',
            'username',
            'dob',
            'followed',          
        )

    def get_followed(self,instance):
        request = self.context.get('request')
        if Followers.objects.filter(follower=request.user,following = instance.user).exists():
            follow=Followers.objects.get(follower=request.user,following = instance.user)
            print(follow.follower,request.user)
            if follow.is_accepted == False:
                followed='false'
            else:
                followed = 'true'
        else :
            followed = 'not_send'
        return followed

        