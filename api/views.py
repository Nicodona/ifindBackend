from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics
from rest_framework import status

from .serializers import RegisterSerializer, FoundSerializer, UserSerializer, JobSerializer, ReportSerializer, \
    MessageSerializer
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Register, Found, Job, Report, Message
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
# about img_extraction
import base64
import pytesseract
from PIL import Image
import io
from copy import deepcopy

from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import viewsets

#detail logics

# detail for user data
class User_data(APIView):
    def get(self, request, pk):
        user_data = get_object_or_404(Register, pk=pk)
        data = RegisterSerializer(user_data).data
        return Response(data)

# detail for jobs
# class JobDetail(APIView):
#     def get(self, request, pk):
#         user_data = get_object_or_404(Job, pk=pk)
#         data = JobSerializer(user_data).data
#         return Response(data)

#dtail for found_item

# class FoundDetail(APIView):
#     def get(self, request, pk):
#         user_data = get_object_or_404(Found, pk=pk)
#         data = FoundSerializer(user_data).data
#         return Response(data)

class FoundItems(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Found.objects.all()
    serializer_class = FoundSerializer

    def destroy(self, request, *args, **kwargs):
        found = Found.objects.get(pk=self.kwargs["pk"])

        if not found.author == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(self, *args, **kwargs)


class JobItems(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def destroy(self, request, *args, **kwargs):
        job = Job.objects.get(pk=self.kwargs["pk"])

        if not Job.author == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(self, *args, **kwargs)


class Messages(APIView):
    permission_classes = [IsAuthenticated]



class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    def destroy(self, request, *args, **kwargs):
        message = Message.objects.get(pk=self.kwargs["pk"])

        if not message.author == request.user or message.reciever == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(self, *args, **kwargs)


class Reports(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Report.objects.all()[:20]
        data = ReportSerializer(items, many=True).data
        return Response(data)


class CreateJob(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        author = request.user.id
        title = request.data.get('title')
        desc = request.data.get('desc')
        location = request.data.get('location')
        payment = request.data.get('payment')
        number_needed = request.data.get('number_needed')

        data = {'author': author, 'title': title, 'desc': desc, 'location': location, 'payment': payment, 'number_needed': number_needed}
        serializer = JobSerializer(data=data)

        if serializer.is_valid():
            job = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CreateMessage(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         author = request.user.id
#         message = request.data.get('message')
#
#         data = {'author': author, 'message': message}
#
#         serializer = MessageSerializer(data=data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             print(serializer.errors)
#             return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateReport(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        author = request.user.id
        account = request.data.get('account')
        reason = request.data.get('reason')

        data = {'author': author, 'account': account, 'reason': reason}
        serializer = ReportSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateProfile(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        userid = request.user.id
        name = request.data.get('name')
        region = request.data.get('region')
        location = request.data.get('location')
        picture = request.data.get('picture')
        profession = request.data.get('profession')

        data = {'userid': userid, 'name': name, 'region':region, 'location': location, 'picture': picture, 'profession': profession}
        serializer = RegisterSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
class CreateItem(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        author = request.user.id
        img = request.data.get('image')
        #
        # image = deepcopy(img)

        # try:
        # image = request.FILES['image']
        # image_bytes = base64.b64encode(img)
        # image_bytes = base64.b64decode(img)
        # image = Image.open(io.BytesIO(image_bytes))
        # #     im = Image.open(image)
        # #
        # # except (KeyError, IOError):
        # #    pass
        #
        # # #extract img with pytesseract
        # description = pytesseract.image_to_string(image, config=r" --psm 6, --oem 3")

        # print(description)
        data = {'author': author, 'image': img}
     #   data = {'author': author, 'image':im, 'description': description}
        serializer = FoundSerializer(data=data)

        if serializer.is_valid():
            found = serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    for user in User.objects.all():
        Token.objects.get_or_create(user=user)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            print('LOGIN SUCESS')
            return Response({"token": user.auth_token.key, 'status': status.HTTP_200_OK})
        else:
            return Response({"error": "wrong credential", 'status': status.HTTP_400_BAD_REQUEST})
