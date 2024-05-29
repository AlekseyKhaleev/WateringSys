from datetime import datetime, timedelta

from django.db.models import Avg, Max, Min
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import HttpResponseRedirect
from .forms import PumpForm
from .models import PumpingValueModel

from Django_side.TEMPapp.serializers import *


###############################
def graphic_month(request):
    current_time = datetime.now()
    title = "за последний месяц"

    def init_data_labels(_val_type):
        data, labels, min, avg, max, day, hour, minute, count, opcount = [], [], "", "", "", "", "", "", 0, 0

        queryset = CSMSModel.objects.filter(DATE__year=current_time.year, DATE__month=current_time.month)

        for query in queryset:
            labels.append(str(query.DATE.strftime("%Y-%m-%d %H:%M")))
            if _val_type == "TEMPERATURE":
                data.append(query.TEMPERATURE)
            else:
                data.append(query.HUMIDITY)

        min_b = str(queryset.aggregate(Min(_val_type)))[len(_val_type) + 9:len(_val_type) + 14]
        min = min_b[:min_b.find('.')]
        avg_b = str(queryset.aggregate(Avg(_val_type)))[len(_val_type) + 9:len(_val_type) + 14]
        avg = avg_b[:avg_b.find('.')]
        max_b = str(queryset.aggregate(Max(_val_type)))[len(_val_type) + 9:len(_val_type) + 14]
        max = max_b[:max_b.find('.')]
        count = queryset.count()
        day = str(current_time.strftime("%d"))
        hour = str(current_time.strftime("%H"))
        minute = str(current_time.strftime("%M"))
        opcount = int(day) * 24 * 60 + int(hour) * 60 + int(minute)  # day *24+60 + HORA*60 + MIN

        return {'data': data, 'labels': labels, 'min': min, 'avg': avg, 'max': max, 'count': count, 'day': day,
                'hour': hour, 'minute': minute, 'opcount': opcount}

    # t_data = init_data_labels("TEMPERATURE")
    h_data = init_data_labels("HUMIDITY")

    # return render(request, 'CSMSview.html', {'t_data': t_data, 'h_data': h_data, 'title': title})
    return render(request, 'CSMSview.html', {'h_data': h_data, 'title': title})


###############################FUNCIONA
def graphic_24h(request):
    current_time = datetime.now()
    title = "за последние 24 часа"

    def init_data_labels(_val_type):
        data, labels, min, avg, max, day, hour, minute, count, opcount = [], [], "", "", "", "", "", "", 0, 0
        time_flag = current_time - timedelta(hours=24)
        queryset = CSMSModel.objects.filter(DATE__range=(time_flag, current_time))

        for query in queryset:
            labels.append(str(query.DATE.strftime("%Y-%m-%d %H:%M")))
            if _val_type == "TEMPERATURE":
                data.append(query.TEMPERATURE)
            else:
                data.append(query.HUMIDITY)

        min_b = str(queryset.aggregate(Min(_val_type)))[len(_val_type) + 9:len(_val_type) + 14]
        min = min_b[:min_b.find('.')]
        avg_b = str(queryset.aggregate(Avg(_val_type)))[len(_val_type) + 9:len(_val_type) + 14]
        avg = avg_b[:avg_b.find('.')]
        max_b = str(queryset.aggregate(Max(_val_type)))[len(_val_type) + 9:len(_val_type) + 14]
        max = max_b[:max_b.find('.')]
        count = queryset.count()
        day = str(current_time.strftime("%d"))
        hour = str(current_time.strftime("%H"))
        minute = str(current_time.strftime("%M"))
        opcount = 1440

        return {'data': data, 'labels': labels, 'min': min, 'avg': avg, 'max': max, 'count': count, 'day': day,
                'hour': hour, 'minute': minute, 'opcount': opcount}

    # t_data = init_data_labels("TEMPERATURE")
    h_data = init_data_labels("HUMIDITY")

    # return render(request, 'CSMSview.html', {'t_data': t_data, 'h_data': h_data, 'title': title})
    return render(request, 'CSMSview.html', {'h_data': h_data, 'title': title})


###############################
def graphic_hour(request):
    if request.method == 'POST':
        form = PumpForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            value = form.save(commit=False)
            value.save()
        else:
            pass
    else:
        form = PumpForm()
    current_time = datetime.now()
    title = "за последний час"

    def init_data_labels(_val_type):
        data, labels, min, avg, max, day, hour, minute, count, opcount = [], [], "", "", "", "", "", "", 0, 0
        time_flag = current_time - timedelta(hours=1)
        queryset = CSMSModel.objects.filter(DATE__range=(time_flag, current_time))

        for query in queryset:
            labels.append(str(query.DATE.strftime("%Y-%m-%d %H:%M")))
            if _val_type == "TEMPERATURE":
                data.append(query.TEMPERATURE)
            else:
                data.append(query.HUMIDITY)

        min_b = str(queryset.aggregate(Min(_val_type)))[len(_val_type) + 9:len(_val_type) + 14]
        min = min_b[:min_b.find('.')]
        avg_b = str(queryset.aggregate(Avg(_val_type)))[len(_val_type) + 9:len(_val_type) + 14]
        avg = avg_b[:avg_b.find('.')]
        max_b = str(queryset.aggregate(Max(_val_type)))[len(_val_type) + 9:len(_val_type) + 14]
        max = max_b[:max_b.find('.')]

        count = queryset.count()
        day = str(current_time.strftime("%d"))
        hour = str(current_time.strftime("%H"))
        minute = str(current_time.strftime("%M"))
        opcount = 60

        return {'data': data, 'labels': labels, 'min': min, 'avg': avg, 'max': max, 'count': count, 'day': day,
                'hour': hour, 'minute': minute, 'opcount': opcount}

    h_data = init_data_labels("HUMIDITY")

    return render(request, 'CSMSview.html', {'h_data': h_data, 'title': title, 'form': form})


@csrf_exempt
def csms_serializer_setter(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = CSMSModel.objects.all()
        serializer = CSMSSerializerGet(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CSMSSerializerPost(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def avg_serializer_getter(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        current_time = datetime.now()
        full_data, avg, _val_type = [], "", "HUMIDITY"
        time_flag = current_time - timedelta(minutes=10)
        queryset = CSMSModel.objects.filter(DATE__range=(time_flag, current_time))

        for query in queryset:
            full_data.append(query.HUMIDITY)
        avg_b = str(queryset.aggregate(Avg(_val_type)))[len(_val_type) + 1 + 9:len(_val_type) + 14]
        avg = avg_b[:avg_b.find('.')]
        print(avg)
        if int(avg) < 70:
            json_data = {"avg_hum": avg, "pump_flag": 1}
            return JsonResponse(json_data, safe=False)
        else:
            json_data = {"avg_hum": avg, "pump_flag": 0}
            return JsonResponse(json_data, safe=False)


def get_pump_value(request):
    if request.method == 'POST':
        form = PumpForm(request.POST)
        if form.is_valid():
            return request.META.get('HTTP_REFERER')
    else:
        form = PumpForm()
    return render(request, 'CSMSview.html', {'form': form})


def home(request):
    return render(request, 'home.html')
