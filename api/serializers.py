from rest_framework import serializers
from .models import Found, Register,Job, Report, Message
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import pytesseract
from PIL import Image
from copy import deepcopy

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = '__all__'


class FoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Found
        fields = '__all__'
class FoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Found
        fields = ['author', 'image']



    # def create(self, validated_data):
    #     image = deepcopy(validated_data.get("image"))
    #     print(image)
    #     description = pytesseract.image_to_string(validated_data['image'])
    #     print(description)
    #     return Found.objects.create(description=description, **validated_data)


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email= validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
