from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'avatar', 'bio', 'location', 'website', 'birth_date')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        email = validated_data.get('email', '')
        password = validated_data.pop('password')
        username = email.split('@')[0]
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
