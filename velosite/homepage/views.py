from datetime import datetime, timedelta

import pytz as pytz
from django.shortcuts import render, redirect

# Create your views here.
from .forms import VeloStationForm, BicycleForm
from .models import BicycleStation, Bicycle, Order
import pendulum as pendulum


def getFormData(form, fieldName):
    return form.cleaned_data.get(fieldName)


def bicycleStationList(request):
    data = {
        'bikeStations': BicycleStation.objects.all()
    }
    return render(request, 'homePage/stations.html', data)


def trolley(request):
    myOrders = list()
    allOrders = Order.objects.all()
    totalPrice = 0
    for order in allOrders:
        if request.user.id == order.user_id and order.bike.status == "free":
            myOrders.append(order)
            totalPrice += order.price
    data = {
        "totalPrice": totalPrice,
        "trolley": myOrders
    }
    return render(request, 'homePage/trolley.html', data)


def bicycleList(request, station_id):
    station = BicycleStation.objects.get(id=station_id)
    data = {
        'bikeStation': station,
        'bikes': station.bicycle_set.all()
    }
    return render(request, 'homePage/bicycles.html', data)


def bikeDetails(request, station_id, bike_id):
    station = BicycleStation.objects.get(id=station_id)
    data = {
        'bikeStation': station,
        'bike': station.bicycle_set.get(id=bike_id)
    }
    return render(request, 'homePage/bikeDetails.html', data)


def __orderInTrolley(bike_id, user_id):
    try:
        if type(Order.objects.get(bike_id=bike_id, user_id=user_id)) is Order:
            return True
    except:
        return False


def allBikes(request):
    data = {
        'bikeStation': BicycleStation(name="All bikes"),
        'bikes': Bicycle.objects.all()
    }
    return render(request, 'homePage/bicycles.html', data)


def actions(request, station_id, bike_id, action):
    match action:
        case "to_trolley":
            if __orderInTrolley(bike_id, request.user.id) is False:
                bike = Bicycle.objects.get(id=bike_id)
                order = Order(user_id=request.user.id, usageTime=1, price=bike.price)
                bike.order_set.add(order, bulk=False)
            return redirect(bicycleList, station_id)
        case "delete_bike":
            Bicycle.objects.get(id=bike_id).delete()
            return redirect(bicycleList, station_id)
        case "update_bike":
            error = ''
            if request.method == 'POST' and request.user.is_staff:
                form = BicycleForm(request.POST, request.FILES)
                if form.is_valid():
                    Bicycle.objects.get(id=bike_id).delete()
                    BicycleStation.objects.get(id=station_id) \
                        .bicycle_set \
                        .create(name=getFormData(form, 'name'),
                                photo=getFormData(form, 'photo'),
                                usages=getFormData(form, 'usages'),
                                description=getFormData(form, 'description'),
                                price=getFormData(form, 'price'))
                    return redirect('homePage')
                else:
                    error = 'Entered data is incorrect'
            form = BicycleForm(**{'bike': Bicycle.objects.get(id=bike_id)})
            data = {
                'form': form,
                'error': error
            }
            return render(request, 'homePage/bikeForm.html', data)


def addBike(request, station_id, action):
    error = ''
    if request.method == 'POST' and request.user.is_staff:
        form = BicycleForm(request.POST, request.FILES)
        if form.is_valid():
            BicycleStation.objects.get(id=station_id) \
                .bicycle_set \
                .create(name=getFormData(form, 'name'),
                        photo=getFormData(form, 'photo'),
                        usages=getFormData(form, 'usages'),
                        description=getFormData(form, 'description'),
                        price=getFormData(form, 'price'))
            return redirect('homePage')
        else:
            error = 'Entered data is incorrect'
    form = BicycleForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'homePage/bikeForm.html', data)


def orderActions(request, order_id, action, in_trolley):
    order = Order.objects.get(id=order_id)
    orderRentTime = order.usageTime
    match action:
        case "hoursUP":
            if orderRentTime <= 50:
                orderRentTime += 1
            order.usageTime = orderRentTime
            order.price = order.bike.price * order.usageTime
            order.save()
        case "hoursDOWN":
            if order.usageTime > 1:
                order.usageTime -= 1
            order.price = order.bike.price * order.usageTime
            order.save()
        case "cancel":
            order.delete()
        case "return-bike":
            bike = order.bike
            bike.status = "free"
            bike.user = 0
            bike.usages += 1
            bike.save()
            order.delete()
    return redirect(trolley)


def addStation(request):
    error = ''
    if request.method == 'POST' and request.user.is_staff:
        form = VeloStationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homePage')
        else:
            error = 'Entered data is incorrect'
    form = VeloStationForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'homePage/addStation.html', data)


def makeOrder(request, trolley, total_price):
    myOrders = list()
    for order in Order.objects.all():
        if order.user_id == request.user.id or request.user.is_staff:
            if order.bike.status == "free":
                now = datetime.now()
                return_time = now + timedelta(hours=order.usageTime)
                order.returnTime = return_time
                order.bike.status = "in use"
                order.bike.user = request.user.id
                order.bike.save()
                order.save()
            myOrders.append(order)

    data = {
        "orders": myOrders,
        "total_price": total_price
    }
    return render(request, 'homePage/rentedBikes.html', data)


def station_actions(request, station_id, action):
    if action == 'update':
        error = ''
        if request.method == 'POST' and request.user.is_staff:
            form = VeloStationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('homePage')
            else:
                error = 'Entered data is incorrect'
        form = VeloStationForm(**{'station': BicycleStation.objects.get(id=station_id)})
        data = {
            'form': form,
            'error': error
        }
        return render(request, 'homePage/addStation.html', data)
    elif action == 'delete':
        BicycleStation.objects.get(id=station_id).delete()
        return redirect('homePage')


def auth(request):
    return render(request, 'registration/login.html')
