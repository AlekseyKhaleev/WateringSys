from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("graphic_hour", graphic_hour, name="HOUR"),
    path("graphic_24h", graphic_24h, name="DAY"),
    path("graphic_month", graphic_month, name="MONTH"),
    path('snippets/', csms_serializer_setter, name="DataList"),
    path('get_average/', avg_serializer_getter, name='AvgHum'),
    path('pumping-value/', get_pump_value, name='pumping_value')

    # path('humsnippets/', hum_serializer_setter, name ="Listado"),
    # path("menu", home, name="menu"),# asigana la url menu, llama a la vista menu, y le da el nombre de menu

]
