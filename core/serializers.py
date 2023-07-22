from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import (
    Document,
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "is_staff"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        file_size = data['file'].size
        file_format = data['file_format']
        file_name_length = len(str(data['file']).split('.'))
        file_ext = str(data['file']).split('.')[file_name_length-1]
        if(data['owner'] != user):
            raise serializers.ValidationError({"Error": "You must provide your user id as owner."})
        if file_size > 5242880:
            raise serializers.ValidationError({"Error": "File size must be less than 5 mb."})
        if file_ext != file_format:
            raise serializers.ValidationError({"Error": "File format and file type must be the same."})
        return data
