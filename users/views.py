from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny)

    @api_view(['POST'])
    def signup(request):
        print(request)
        if request.method == 'POST':
            serializer = CustomUserSerializer(data=request.data)
            data = {}

            if serializer.is_valid():
                account = serializer.save()
                data['response'] = 'Successfully registered a new user'
                data['email'] = account.email
                data['username'] = account.username
            else:
                data = serializer.errors

            return Response(data)

    @csrf_exempt
    @api_view(['POST'])
    def login(request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not password:
            return Response(
                {'error': 'Please provide a valid password'},
                status=HTTP_400_BAD_REQUEST
            )
        else:
            if not username and email:
                username = CustomUser.objects.get(email=email).username
            else:
                if not username and not email:
                    return Response(
                        {'error': 'Please provide a username or email'},
                        status=HTTP_400_BAD_REQUEST
                    )

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {'error': 'Invalid Credentials'},
                status=HTTP_404_NOT_FOUND
            )

        token, _ = Token.objects.get_or_create(user=user)

        serialized_user = CustomUserSerializer(user)

        return Response(
            {'token': token.key, 'user': serialized_user.data},
            status=HTTP_200_OK
        )
