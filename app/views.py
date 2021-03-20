from rest_framework import status
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.generics import GenericAPIView
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RefreshTokenSerializer


class UserRegisterView(APIView):

    def post(self, request):
        try:
            data = request.data
            user_instance = User.objects.filter(email=data.get("email")).first()
            if user_instance:
                return Response(data="User already exists!!!!", status=status.HTTP_200_OK)
            else:
                s = UserSerializer(data=request.data)
            if s.is_valid(raise_exception=True):
                s.save()
                return Response(data=s.data, status=status.HTTP_201_CREATED)
        except (KeyError, ValidationError, Exception) as ex:
            return Response(data=ex.args, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):

    def post(self, request):
        try:
            data = request.data
            user_instance = User.objects.filter(phone=data.get("phone")).first()
            if not user_instance:
                raise APIException(detail="user does not exists!!!!", code=status.HTTP_400_BAD_REQUEST)
            if user_instance:
                s = UserSerializer(instance=user_instance)
                token_serializer = TokenObtainPairSerializer.get_token(user_instance)
                data = s.data
                data.update(token=str(token_serializer.access_token))
                return Response(data=data, status=status.HTTP_200_OK)
        except (KeyError, ValidationError) as ex:
            return Response(data=ex.args, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer

    def post(self, request, *args):
        user = request.user
        user_instance = User.objects.get(email=user)
        refresh_token = RefreshToken.for_user(user_instance)
        data = {'refresh': refresh_token}
        refresh_token_serializer = TokenRefreshSerializer(data)
        token_data = refresh_token_serializer.data
        data = {'refresh': token_data['refresh']}
        sz = self.get_serializer(data=data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)