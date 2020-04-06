import requests

from .models import City


def is_city_in_db(new_city):

    existing_city_count = City.objects.filter(name=new_city).count()
    if existing_city_count == 0:
        return False
    else:
        return True

def is_city_exist(new_city):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=fca2224ce6af72370f76db5917959647"
    r = requests.get(url.format(new_city)).json()
    if r["cod"] == 200:
        return True
    else:
        return False

def is_city_valid(new_city):

    if is_city_in_db(new_city):
        return {"action":False, "err_msg":"City already exists in the database!"}
    else:
        if is_city_exist(new_city):
            return {"action":True}
        else:
            return {"action":False, "err_msg":"City does not exist in the world!"}