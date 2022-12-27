from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from . import views

urlpatterns = [
                  path('', views.bicycleStationList, name="homePage"),
                  path('bikes/', views.allBikes, name="bikes"),
                  path('<int:station_id>', views.bicycleList, name="bicycles"),
                  path('<int:station_id>/<int:bike_id>', views.bikeDetails, name="bikeDetails"),
                  path('<int:station_id>/<int:bike_id>/<str:action>', views.actions, name="actions"),
                  path('trolley/', views.trolley, name="trolley"),
                  path('<int:station_id>/<str:action>', views.addBike, name="add_bike"),
                  path('velostation <int:station_id>/<str:action>', views.station_actions, name="stationActions"),
                  path('<int:order_id>/<str:action>/<str:in_trolley>', views.orderActions, name="orderAction"),
                  path('create_velostation/', views.addStation, name="add_station"),
                  path('<str:trolley>/<int:total_price>', views.makeOrder, name="make_order"),
                  path('/login', views.auth,name= 'login/out')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
