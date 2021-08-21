from main.serializers import OtherReportSerializer
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .models import *
# from numpy.lib.type_check import _imag_dispatcher
# from werkzeug.utils import escape, secure_filename
# from tensorflow.keras.models import load_model
# import matplotlib.pyplot as plt
# import cv2
# import numpy as np
# rest framework
from rest_framework import serializers, status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# resnet_chest = load_model(str(settings.BASE_DIR) + "\main\static\models\\resnet_chest.h5")
# vgg_chest = load_model(str(settings.BASE_DIR) + "\main\static\models\\vgg_chest.h5")
# inception_chest  = load_model(str(settings.BASE_DIR) + "\main\static\models\\inceptionv3_chest.h5")
# xception_chest  = load_model(str(settings.BASE_DIR) + "\main\static\models\\xception_chest.h5")


# Create your views here.
def home(request):
    context = {"title":"Home | Covid Test"}
    return render(request, 'home.html', context)


# def detectchest(request):
#     if not request.user.is_authenticated:
#         return redirect('/login')
#     if request.method == "POST":
#         image = request.FILES.get('file')
#         covid_user = CovidTestImage(
#             user = request.user,
#             chest_xray = image,
#         )
#         covid_user.save()
#         img_path = str(settings.BASE_DIR) + "\media\chestXray\{}".format(str(image))
#         # print(img_path)
#         image = cv2.imread(img_path)
#         # print(image)
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         image = cv2.resize(image, (224, 224))
#         image = np.array(image) / 255
#         image = np.expand_dims(image, axis=0)

#         covid_count_neg = 0
#         covid_count_pos = 0
#         # resnet prediction
#         resnet_pred = resnet_chest.predict(image)
#         probability = resnet_pred[0]
#         if probability[0] > 0.5:
#             covid_count_pos += 1
#             resnet_chest_pred = str('{}% COVID'.format(round(probability[0]*100),2))
#         else:
#             covid_count_neg +=1
#             resnet_chest_pred = str('{}% NonCovid'.format(round((1 - probability[0]) * 100),2))

#         # vgg prediction
#         vgg_pred = vgg_chest.predict(image)
#         probability = vgg_pred[0]
#         if probability[0] > 0.5:
#             covid_count_pos += 1
#             vgg_chest_pred = str('{}% COVID'.format(round(probability[0]*100),2))
#         else:
#             covid_count_neg +=1
#             vgg_chest_pred = str('{}% NonCovid'.format(round((1 - probability[0]) * 100),2))
        
#         # inception prediction
#         inception_pred = inception_chest.predict(image)
#         probability = inception_pred[0]
#         if probability[0] > 0.5:
#             covid_count_pos += 1
#             inception_chest_pred = str('{}%  COVID'.format(round(probability[0]*100),2))
#         else:
#             covid_count_neg +=1
#             inception_chest_pred = str('{}% NonCovid'.format(round((1 - probability[0]) * 100),2))

#         # xception prediction
#         xception_pred = xception_chest.predict(image)
#         probability = xception_pred[0]
#         if probability[0] > 0.5:
#             covid_count_pos += 1
#             xception_chest_pred = str('{}% COVID'.format(round(probability[0]*100),2))
#         else:
#             covid_count_neg +=1
#             xception_chest_pred = str('{}% NonCovid'.format(round((1 - probability[0]) * 100),2))

#         if covid_count_pos > covid_count_neg:
#             res = True
#         else:
#             res = False

#         covid_result = CovidResultData(
#             user = request.user,
#             resnet = resnet_chest_pred,
#             vgg = vgg_chest_pred,
#             inception = inception_chest_pred,
#             exception = xception_chest_pred,
#             covid_result = res
#         )
#         covid_result.save()

#         context = {
#             "title":"Covid Result | Covid Test",
#             "resnet_chest_pred":resnet_chest_pred,
#             "vgg_chest_pred":vgg_chest_pred,
#             "inception_chest_pred":inception_chest_pred,
#             "xception_chest_pred": xception_chest_pred,

#         }
#         return render(request, 'results.html', context)
#     context = {
#         "title":"Detect Chest | Covid Test",
#     }
#     return render(request, 'detectcovid.html', context)


def myregistration(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        user = User(
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            email = request.POST.get('email'),
            age = request.POST.get('age'),
            address = request.POST.get('address'),
        )
        password = request.POST.get('password')
        confirm_password = request.POST.get('cpassword')
        if password == confirm_password:
            user.set_password(password)
            user.save()
            Token.objects.create(user=user)
            login(request, user)
            return redirect('/')
        else:
            return redirect('/register')

    context = {"title":"Registraion  | Covid Test"}
    return render(request, 'registration.html', context)


def mylogin(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        if email != "" and password != "":
            user = authenticate(email=email, password=password)
            if user != None:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/login')
    context = {"title":"Login | Covid Test"}
    return render(request, 'login.html',context)


def mylogout(request):
    logout(request)
    return redirect('/login')



class ReportViewSet(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):
        pulse_rate = request.data.get('pulse_rate')
        saturation_ratio = request.data.get('saturation_ratio')
        oxygen_level = request.data.get('oxygen_level')
        temperature = request.data.get('temperature')
        userid = request.user.id
        if not pulse_rate:
            return Response({'pulse_rate': 'No pulse rate detected'}, status=status.HTTP_400_BAD_REQUEST)
        if not saturation_ratio:
            return Response({'saturation_ratio': 'No saturation ratio detected'}, status=status.HTTP_400_BAD_REQUEST)
        if not oxygen_level:
            return Response({'oxygen_level': 'No oxygen level detected'}, status=status.HTTP_400_BAD_REQUEST)
        if not temperature:
            return Response({'temperature': 'No temperature detected'}, status=status.HTTP_400_BAD_REQUEST)
        if not userid:
            return Response({'userid': 'No user detected'}, status=status.HTTP_400_BAD_REQUEST)


        report = OtherReports(
            pulse_rate = pulse_rate,
            saturation_ratio = saturation_ratio,
            oxygen_level = oxygen_level,
            temperature = temperature,
            user = request.user
        )
        report.save()
        serializer = OtherReportSerializer(report)

        return Response({'message': 'New Report Created', 'data': serializer.data}, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        queryset = OtherReports.objects.filter(user=request.user)
        print(queryset)
        serializer = OtherReportSerializer(queryset, many=True)
        return Response({'message': 'Reports', 'data': serializer.data}, status=status.HTTP_200_OK)
