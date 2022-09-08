from enum import auto
from urllib import response
from accounts.models import Profile
from api.v1.accounts import serializers
from api.v1.posts.serializers import CommentsViewSerializer, PostCommentSerializer, PostSerializer, PostViewSerializer
from posts.models import PostComments, PostLikes, Posts
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from api.v1.main.functions import randomnumber, validate_password, generate_serializer_errors
from django.contrib.auth.hashers import make_password
from main.encryption import encrypt
from api.v1.main.functions import get_auto_id
from api.v1.main.functions import get_auto_id


@api_view(['POST'])
def create_post(request):
    profile = Profile.objects.get(user = request.user)
    serialized = PostSerializer(data = request.data)
    if serialized.is_valid():
        post = request.data['post']
        description = request.data['description']
        post = Posts.objects.create(
            auto_id = get_auto_id(Posts),
            creator = request.user,
            updater = request.user,
            user = profile,
            post = post,
            description=description,
        )
        response_data={
            'StatusCode':6000,
            'data':{
                'title':'success',
                'message':'succesfully posted'
            }
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Validation Error",
                "message": generate_serializer_errors(serialized._errors)
            }
        }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_posts(request):
    instance = Posts.objects.all()
    serialized = PostViewSerializer(
        instance,
        many = True,
        context = {
            "request":request
        }
    ).data
    response_data={
        'StatusCode':6000,
        'data':{
            'title':'success',
            'data':serialized
        }
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def like_post(request,pk):
    profile = Profile.objects.get(user = request.user)
    post = Posts.objects.get(pk = pk)
    if PostLikes.objects.filter(post = post,liked_user = profile).exists():
        like =PostLikes.objects.filter(post = post,liked_user = profile).delete()
        response_data={
            'StatusCode':6000,
            'data':{
                'title':'success',
                'message':'disliked'
            }
        }
    else:
        like = PostLikes.objects.create(
            auto_id = get_auto_id(PostLikes),
            creator = request.user,
            updater = request.user,
            post = post,
            liked_user = profile

        )
        response_data={
            'StatusCode':6000,
            'data':{
                'title':'success',
                'message':'liked'
            }
        }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def comment_post(request,pk):
    serialized = PostCommentSerializer(data = request.data)
    if serialized.is_valid():
        comment = request.data['comment']
        profile = Profile.objects.get(user = request.user)
        post = Posts.objects.get(pk=pk)
        comment = PostComments.objects.create(
            auto_id = get_auto_id(PostComments),
            creator = request.user,
            updater = request.user,
            comment = comment,
            post = post,
            commented_user = profile,
        )
        response_data = {
            'StatusCode':6000,
            'data':{
                "title":'success',
                "message":"successfully commented"
            }
        }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Validation Error",
                "message": generate_serializer_errors(serialized._errors)
            }
        }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def comment_view(request,pk):
    post = Posts.objects.get(pk=pk)
    instance = PostComments.objects.filter(post=post)
    serialized = CommentsViewSerializer(
        instance,
        many = True,
        context = {
            "request":request
        }
    ).data
    
    response_data={
        'StatusCode':6000,
        'data':{
            'title':'success',
            'data':serialized
        }
    }
    return Response(response_data, status=status.HTTP_200_OK)