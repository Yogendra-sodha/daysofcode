import requests
import json
my_lat = 36.7201600
my_lon = -4.4203400
param = {
    'lat' : my_lat,
    'lng' : my_lon,
    'formatted' : 0

}

response = requests.get(" https://api.sunrise-sunset.org/json",params=param)

response.raise_for_status()


print(data)
