from ast import If
from curses.ascii import isdigit
import email
from multiprocessing import context
import profile
from sre_constants import SUCCESS
from turtle import right
from urllib import response
from urllib.request import Request
import requests
from django.utils import timezone
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from api.v1.accounts.serializers import RegisterSerializer, UserListSerializer
from accounts.models import Profile
from api.v1.accounts.serializers import LoginSerializer
from api.v1.accounts.serializers import BirthDaySerializer
from api.v1.accounts import serializers
from api.v1.accounts.serializers import MinimalSerializer
from api.v1.main.functions import get_auto_id
from api.v1.accounts.serializers import FollowRequestSerializer
from api.v1.accounts.serializers import FollowRequestListSerializer
from relations.models import Followers
from main.encryption import decrypt

from main.models import Country
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from api.v1.main.functions import randomnumber, validate_password, generate_serializer_errors
from django.contrib.auth.hashers import make_password
from main.encryption import encrypt


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    serializer = RegisterSerializer(data = request.data)
    if serializer.is_valid():
        username = request.data['username']
        password = request.data['password']
        fullname = request.data['fullname']
        phone = request.data['phone']
        print(username,password,fullname,phone)
        if Profile.objects.filter(phone = phone , email = phone,username = username).exists():
            response_data={
                'StatusCode':6001,
                'data':{
                    'title':'message',
                    'message':'already have account'
                }
            }
        else:
            user = User.objects.create_user(
                username = username,
                password = password
            )
            encpass = encrypt(password)
            if phone.isdigit():
                profile = Profile.objects.create(
                    user = user,
                    name = fullname,
                    username = username,
                    password = encpass,
                    phone = phone,
                )
                print(encpass)
            else:
                profile = Profile.objects.create(
                    user = user,
                    name = fullname,
                    password = encpass,
                    email = phone,
                )
            protocol = "http://"
            web_host = request.get_host()
            request_url = protocol + web_host + "/api/v1/accounts/token/"
            response = requests.post(
                        request_url, 
                        data={
                            'username': username,
                            'password': password,
                        },
                    )
            response = response.json()
            response_data={
                'StatusCode':6000,
                'data':{
                    'title':'success',
                    'access': response,  
                }
            }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Validation Error",
                "message": generate_serializer_errors(serializer._errors)
            }
        }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        phone = request.data['phone']
        password = request.data['password']
        if phone.isdigit():
            if Profile.objects.filter(phone=phone).exists():
                profile=Profile.objects.get(phone=phone)
                decrpass=decrypt(profile.password)
                if password == decrpass:
                    protocol = "http://"
                    web_host = request.get_host()
                    request_url = protocol + web_host + "/api/v1/accounts/token/"
                    response = requests.post(
                        request_url, 
                        data={
                            'username': profile.username,
                            'password': password,
                        },
                    )
                    response = response.json()
                    response_data = {
                        "StatusCode": 6000,
                        "data": {
                            "title": "success",
                            "acess": response
                        }
                    }
                else:
                    response_data = {
                        "StatusCode": 6001,
                        "data": {
                            "title": "failed",
                            "message": 'incorrect password'
                        }
                    }
            else:
                response_data = {
                        "StatusCode": 6001,
                        "data": {
                            "title": "failed",
                            "message": 'no profile found on this number'
                        }
                    }
        else:
            if Profile.objects.filter(email=phone).exists():
                profile=Profile.objects.get(email=phone)
                decrpass=decrypt(profile.password)
                if password == decrpass:
                    protocol = "http://"
                    web_host = request.get_host()
                    request_url = protocol + web_host + "/api/v1/accounts/token/"
                    response = requests.post(
                        request_url, 
                        data={
                            'username': profile.username,
                            'password': password,
                        },
                    )
                    response = response.json()
                    response_data = {
                        "StatusCode": 6000,
                        "data": {
                            "title": "success",
                            "acess": response
                        }
                    }
                else:
                    response_data = {
                        "StatusCode": 6001,
                        "data": {
                            "title": "failed",
                            "message": 'incorrect password'
                        }
                    }
            else:
                response_data = {
                        "StatusCode": 6001,
                        "data": {
                            "title": "failed",
                            "message": 'no profile found on this mail'
                        }
                    }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Validation Error",
                "message": generate_serializer_errors(serializer._errors)
            }
        }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def setbirthday(request):
    serializer = BirthDaySerializer(data=request.data)
    if serializer.is_valid():
        dob = request.data['dob']
        user = request.user
        if Profile.objects.filter(user = user).exists():
            profile=Profile.objects.get(user = request.user)
            profile.dob = dob
            profile.is_verified=True
            profile.save()
            response_data={
                'StatusCode':6000,
                'data':{
                    'title':'success',
                    'message':'successfully added birthday'
                }
            }
        else:
            response_data={
                'StatusCode':6001,
                'data':{
                    'message':'no data found'
                }
            }
    else:
        response_data = {
            "StatusCode": 6001,
            "data": {
                "title": "Validation Error",
                "message": generate_serializer_errors(serializer._errors)
            }
        }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def minimals(request):
    if Profile.objects.filter(user = request.user).exists():
        instance = Profile.objects.get(user = request.user)
        serialized = MinimalSerializer(
            instance,
            # many=True,
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
    else:
        response_data={
            'StatusCode':6001,
            'data':{
                'title':'failed',
                'data':'no account not found'
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)


# @api_view(['GET'])
# def users_view(request):
#     instance = Profile.objects.all()
#     serialized = MinimalSerializer(
#         instance,
#         many=True,
#         context={
#             "request":request
#         }
#     ).data
#     response_data={
#         "StatusCode":6000,
#         'data':{
#             'title':'success',
#             'data':serialized
#         }
#     }
#     return Response(response_data,status=status.HTTP_200_OK)


@api_view(['GET'])
def users_view(request):
    profile =request.user
    if Followers.objects.filter(follower=profile,is_accepted = False).exists():
        followers = Followers.objects.filter(follower=profile,is_accepted = False)
        for follower in followers:
            instance = Profile.objects.filter(~Q(user = request.user))
        serialized = UserListSerializer(
            instance,
            many = True,
            context = {
                "request":request
            }
        ).data
        response_data={
            "StatusCode":6000,
            'data':{
                'title':'success',
                'data':serialized
            }
        }
    else:
        instance = Profile.objects.filter(~Q(user = request.user))
        serialized = UserListSerializer(
            instance,
            many=True,
            context = {
                "request":request
            }
        ).data
        response_data = {
            'StatusCode':6000,
            'data':{
                'title':'success',
                'data':serialized
            }
        }
       
    return Response(response_data,status=status.HTTP_200_OK)


@api_view(['GET'])
def send_request(request,pk):
    user = request.user
    send_to = Profile.objects.get(pk = pk)
    if Followers.objects.filter(follower = user,following = send_to.user).exists():
        follower = Followers.objects.get(follower = user,following = send_to.user).delete()
        response_data={
            'StatusCode':6000,
            'data':{
                'title':'success',
                'message':'request cancelled'
            }
        }
    else:
        follower = Followers.objects.create(
            auto_id=get_auto_id(Followers),
            creator = request.user,
            updater =request.user,
            follower = request.user,
            following = send_to.user,
        )
        response_data={
            'StatusCode':6000,
            'data':{
                'title':'Success',
                'message':'Successfully send request'
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)


@api_view(['GET'])
def request_list(request):
    profile = Profile.objects.get(user = request.user)
    if Followers.objects.filter(followed_user = profile).exists():
        instance = Followers.objects.filter(followed_user = profile)
        serialized = FollowRequestSerializer(
            instance,
            many = True,
            context = {
                "request":request
            }
        ).data
        response_data= {
            'data':serialized
        }

    else:
        response_data={
            'StatusCode':6000,
            'data':{
                'title':'success',
                'message':'no request for you'
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)


