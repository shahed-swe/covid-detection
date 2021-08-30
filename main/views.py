from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .models import *
from .serializers import *
from random import randint
from numpy.lib.type_check import _imag_dispatcher
from werkzeug.utils import escape, secure_filename
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import cv2
import numpy as np
# rest framework
from rest_framework import serializers, status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

resnet_chest = load_model(str(settings.BASE_DIR) + "\main\static\models\\resnet_chest.h5")
vgg_chest = load_model(str(settings.BASE_DIR) + "\main\static\models\\vgg_chest.h5")
inception_chest  = load_model(str(settings.BASE_DIR) + "\main\static\models\\inceptionv3_chest.h5")
xception_chest  = load_model(str(settings.BASE_DIR) + "\main\static\models\\xception_chest.h5")


# Create your views here.
def home(request):
    """this view is only for rendering home template"""
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.user.is_authenticated and request.user.is_doctor:
        return redirect('/doctor')
    context = {"title":"Home | Covid Test"}
    return render(request, 'home.html', context)


def doctorhome(request):
    patient = Patient.objects.all()
    condition = PatientCondition.objects.all()
    context = {
        'title': "Doctor Porta | Covid",
        'patients': condition,
    }
    return render(request, 'doctor.html', context)

def patientcondition(request,id):
    patient = Patient.objects.get(pk=id)
    condition = PatientCondition.objects.get(patient=patient)
    context = {
        'title': 'Patient Condition',
        'condition': condition,
        'patient': patient
    }
    return render(request, 'patient_profile.html', context)


def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARD_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip

def detectchest(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.user.is_doctor:
        return redirect('/doctor')
    if request.method == "POST":
        image = request.FILES.get('file')
        covid_user = CovidTestImage(
            user = request.user,
            chest_xray = image,
        )
        covid_user.save()
        img_path = str(settings.BASE_DIR) + "\media\chestXray\{}".format(str(image))
        # print(img_path)
        image = cv2.imread(img_path)
        # print(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))
        image = np.array(image) / 255
        image = np.expand_dims(image, axis=0)

        covid_count_neg = 0
        covid_count_pos = 0
        # resnet prediction
        resnet_pred = resnet_chest.predict(image)
        probability = resnet_pred[0]
        if probability[0] > 0.5:
            covid_count_pos += 1
            resnet_chest_pred = str('{}% Possibility Of Covid'.format(round(probability[0]*100),2))
        else:
            covid_count_neg +=1
            resnet_chest_pred = str('{}% Possibility Of NonCovid'.format(round((1 - probability[0]) * 100),2))

        # vgg prediction
        vgg_pred = vgg_chest.predict(image)
        probability = vgg_pred[0]
        if probability[0] > 0.5:
            covid_count_pos += 1
            vgg_chest_pred = str('{}% Possibility Of COVID'.format(round(probability[0]*100),2))
        else:
            covid_count_neg +=1
            vgg_chest_pred = str('{}% Possibility Of NonCovid'.format(round((1 - probability[0]) * 100),2))
        
        # inception prediction
        inception_pred = inception_chest.predict(image)
        probability = inception_pred[0]
        if probability[0] > 0.5:
            covid_count_pos += 1
            inception_chest_pred = str('{}%  Possibility Of COVID'.format(round(probability[0]*100),2))
        else:
            covid_count_neg +=1
            inception_chest_pred = str('{}% Possibility Of NonCovid'.format(round((1 - probability[0]) * 100),2))

        # xception prediction
        xception_pred = xception_chest.predict(image)
        probability = xception_pred[0]
        if probability[0] > 0.5:
            covid_count_pos += 1
            xception_chest_pred = str('{}% Possibility Of COVID'.format(round(probability[0]*100),2))
        else:
            covid_count_neg +=1
            xception_chest_pred = str('{}% Possibility Of NonCovid'.format(round((1 - probability[0]) * 100),2))

        if covid_count_pos > covid_count_neg:
            res = True
        else:
            res = False

        covid_result = CovidResultData(
            user = request.user,
            resnet = resnet_chest_pred,
            vgg = vgg_chest_pred,
            inception = inception_chest_pred,
            exception = xception_chest_pred,
            covid_result = res
        )
        covid_result.save()

        context = {
            "title":"Covid Result | Covid Test",
            "resnet_chest_pred":resnet_chest_pred,
            "vgg_chest_pred":vgg_chest_pred,
            "inception_chest_pred":inception_chest_pred,
            "xception_chest_pred": xception_chest_pred,

        }
        return render(request, 'results.html', context)
    context = {
        "title":"Detect Chest | Covid Test",
    }
    return render(request, 'detectcovid.html', context)


def myregistration(request):
    """this view is for registering user"""
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        user = User(
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            email = request.POST.get('email'),
            age = request.POST.get('age'),
            address = request.POST.get('address'),
            is_patient = True,
            is_active = True
        )
        password = request.POST.get('password')
        confirm_password = request.POST.get('cpassword')
        if password == confirm_password:
            user.set_password(password)
            user.save()
            Patient.objects.create(user=user)
            Token.objects.create(user=user)
            login(request, user)
            return redirect('/')
        else:
            return redirect('/register')

    context = {"title":"Registraion  | Covid Test"}
    return render(request, 'registration.html', context)

def doctorregistration(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        user = User(
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            email = request.POST.get('email'),
            age = request.POST.get('age'),
            address = request.POST.get('address'),
            is_doctor = True,
            is_active = True,
        )
        password = request.POST.get('password')
        confirm_password = request.POST.get('cpassword')
        if password == confirm_password:
            user.set_password(password)
            user.save()
            Doctor.objects.create(user=user)
            Token.objects.create(user=user)
            login(request, user)
            return redirect('/')
        else:
            return redirect('/register')

    context = {"title":"Doctor Registraion  | Covid Test"}
    return render(request, 'doctorregistration.html', context)


def mylogin(request):
    """this view is only for authenticating a user"""
    if request.user.is_authenticated:
        return redirect('/')
    print(get_ip(request))

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        if email != "" and password != "":
            user = authenticate(email=email, password=password)
            if user != None:
                login(request, user)
                if request.user.is_patient:
                    return redirect('/')
                else:
                    return redirect('/doctor')
            else:
                return redirect('/login')
    context = {"title":"Login | Covid Test"}
    return render(request, 'login.html',context)


def mylogout(request):
    """this is only for deauthenticating a user"""
    logout(request)
    return redirect('/login')



class ReportViewSet(generics.GenericAPIView):
    """this view is for getting sensor data from nodemcu"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )


    """for storing report data temporarily"""
    reportdata = []

    def post(self, request, format=None):
        """this is just a post method
            this will only work when a user try to push a post method
        """
        heart_rate = request.data.get('heart_rate')
        oxygen_level = request.data.get('oxygen_level')
        temperature = request.data.get('temperature')
        if heart_rate != "" and oxygen_level != "" and temperature != "":
            self.reportdata.append({
                "heart_rate" : heart_rate,
                "oxygen_level" : randint(93, 97),
                "temperature" : temperature,
                "report_time": timezone.now
            })

            if float(heart_rate) > 60 and float(heart_rate) < 100 and float(oxygen_level) > 93 and float(oxygen_level) < 97 and float(temperature) > 96 and float(temperature)< 99:
                condition = PatientCondition(
                    patient = request.user,
                    condition_info = "Condition is Good right now",
                )
                condition.save()

            else:
                condition = PatientCondition(
                    patient = request.user,
                    condition_info = "Condition is Good right now",
                )
                condition.save()

            return Response({'message':'new data found'})
        else:
            return Response({'message':'No data'})

    def get(self, request, format=None):
        print(get_ip(request))
        """this will work only when a user try to get those temporary data"""
        newdata = PatientTestData(self.reportdata[::-1], many=True).data
        filterdata = newdata[0:1]
        return Response(filterdata)


def show_report_graph(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.user.is_doctor:
        return redirect('/')
    print(get_ip(request))
    context = {
        "title": "Patient Report Graph",
        "token": Token.objects.get(user=request.user)
    }
    return render(request, 'patient_report_graph.html', context)

def patient_condition(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.user.is_authenticate and request.user.is_patient:
        return redirect('/doctor')
    else:
        context = {
            'title': "Patient List | Covid",
            'patients' : Patient.objects.all(),
        }
        return render('patient_condition.html', context)


def covid_symtoms_check(request):
    context = {
        'title': 'Symptom Check | Covid'
    }
    return render(request, 'covidsymptomcheck.html', context)