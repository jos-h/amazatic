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
            if 'phone' not in data:
                raise APIException(detail="Phone field is required!!!!", code=status.HTTP_400_BAD_REQUEST)
            user_instance = User.objects.filter(phone=data["phone"]).first()
            if not user_instance:
                raise APIException(detail="user does not exists!!!!", code=status.HTTP_400_BAD_REQUEST)
            is_validate = self.validate_password(data, user_instance)
            if user_instance and is_validate:
                s = UserSerializer(instance=user_instance, data=data)
                s.is_valid(raise_exception=True)
                token_serializer = TokenObtainPairSerializer.get_token(user_instance)
                data = s.data
                data.update(token=str(token_serializer.access_token))
                return Response(data=data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(data=ex.args, status=status.HTTP_400_BAD_REQUEST)

    def validate_password(self, data, user):
        msg = "Password field is required!!!"
        errors = dict()
        try:
            password = data['password']
            is_validate = user.check_password(password)
            if not is_validate:
                errors['password'] = 'Incorrect password'
                if errors:
                    raise ValidationError(errors)
            return is_validate
        except KeyError as e:
            raise APIException(detail=msg, code=status.HTTP_400_BAD_REQUEST)


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
