from rest_framework.serializers import ModelSerializer, Serializer, CharField
from .models import User, University, Program
from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UniversitySerializer(ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class ProgramSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RefreshTokenSerializer(Serializer):
    refresh = CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        print("============", self.token)
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
