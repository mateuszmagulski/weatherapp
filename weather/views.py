import requests

from django.shortcuts import render, redirect

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import City
from .forms import CityForm
from .serializers import CitySerializer
from .services import is_city_valid

def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=fca2224ce6af72370f76db5917959647"

    message = ""
    message_class = ""

    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data["name"].title()

            check_city = is_city_valid(new_city)
            
            if check_city["action"]:
                City.objects.create(name=new_city)
                message = "City added successfully!"
                message_class = "is-success"
            else:
                message = check_city["err_msg"]
                message_class = "is-danger"

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        
        r = requests.get(url.format(city)).json()
        city_weather = {
            "pk": city.pk,
            "city": city.name,
            "temperature": r["main"]["temp"],
            "description": r["weather"][0]["description"],
            "icon": r["weather"][0]["icon"],
        }

        weather_data.append(city_weather)

    context = {
        "weather_data":weather_data, 
        "form":form,
        "message":message,
        "message_class":message_class
        }
    return render(request, 'weather/weather.html', context)

def delete_city(request, pk):
    
    City.objects.get(pk=pk).delete()

    return redirect("index")

@api_view(["GET"])
def api_overviwe(request):
    api_urls={
        "List": "/api/list/",
        "Detail": "/api/detail/<int:pk>",
        "Create": "/api/create/",
        "Update": "/api/update/<int:pk>",
        "Delete": "/api/delete/<int:pk>"
    }
    return Response(api_urls)

@api_view(["GET"])
def api_list(request):
    
    cities = City.objects.all()
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def api_details(request, pk):

    city = City.objects.get(pk=pk)
    serializer = CitySerializer(city, many=False)
    return Response(serializer.data)

@api_view(["POST"])
def api_create(request):

    message = ""

    serializer = CitySerializer(data=request.data)

    if serializer.is_valid():
        
        new_city = request.data["name"].title()

        check_city = is_city_valid(new_city)
            
        if check_city["action"]:
            City.objects.create(name=new_city)
            message = "City added successfully!"
        else:
            message = check_city["err_msg"]

    return Response(message)

@api_view(["POST"])
def api_update(request, pk):

    message = ""

    city = City.objects.get(pk=pk)
    serializer = CitySerializer(instance=city, data=request.data )

    if serializer.is_valid():
        new_city = request.data["name"].title()
        
        check_city = is_city_valid(new_city)
            
        if check_city["action"]:
            City.objects.create(name=new_city)
            message = "City added successfully!"
        else:
            message = check_city["err_msg"]

    return Response(message)

@api_view(["DELETE"])
def api_delete(request, pk):
    city = City.objects.get(pk=pk)
    city.delete()
    return Response("City deleted succesfully!")