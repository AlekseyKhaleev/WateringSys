from rest_framework import serializers
from .models import CSMSModel
# from .models import DHT11Model
# from .models import HumModel


class CSMSSerializerPost(serializers.ModelSerializer):  # POST

    class Meta:
        model = CSMSModel
        fields = ["HUMIDITY"]


class CSMSSerializerGet(serializers.ModelSerializer):  # GET

    class Meta:
        model = CSMSModel
        fields = ["HUMIDITY", "DATE"]


# class HumSerializerPost(serializers.ModelSerializer):  # POST
#
#     class Meta:
#         model = HumModel
#         fields = ["TEMPERATURE", "HUMIDITY"]
#
#
# class HumSerializerGet(serializers.ModelSerializer):  # GET
#
#     class Meta:
#         model = HumModel
#         fields = ["HUMIDITY", "DATE"]

        # cd /
        # python3 manage.py shell
        # from INPUT.models import T_Vs_t
        # from INPUT.serializers import Temp_serializer
        # from rest_framework.renderers import JSONRenderer
        # from rest_framework.parsers import JSONParser
        # escribir = T_Vs_t(TEMPERATURA= "20")
        # escribir.save()
        # serializer = Temp_serializer(escribir)
        # serializer.data

        # content = JSONRenderer().render(serializer.data)
        # content

        # serializer = Temp_serializer(T_Vs_t.objects.all(), many=True)
